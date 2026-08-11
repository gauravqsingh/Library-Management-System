from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from accounts.models import UserLibraryAccount
from transactions.constants import BORROWED, RETURN
from transactions.models import Transaction
from . import forms, models


def borrowed_mail(user, amount, subject, template, current_balance):
    message = render_to_string(
        template,
        {
            'user': user,
            'amount': amount,
            'current_balance': current_balance,
        },
    )
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


@login_required
def book_detail(request, book_id):
    book = models.Book.objects.get(id=book_id)
    user = request.user
    user_account = UserLibraryAccount.objects.filter(user=user).first()
    borrowers_list = []
    return_list = []

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.book = book
            new_comment.user = user
            new_comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('book_detail', book_id=book.id)

        if 'borrow' in request.POST:
            if not user_account:
                messages.error(
                    request,
                    'You need a library account to borrow books. Please contact admin.',
                )
                return redirect('book_detail', book_id=book.id)

            if user_account.balance < book.price:
                messages.error(
                    request, 'You do not have enough balance to borrow this book.'
                )
                return redirect('book_detail', book_id=book.id)

            user_account.balance -= Decimal(str(book.price))
            user_account.save()

            Transaction.objects.create(
                account=user_account,
                amount=book.price,
                balance_after_transaction=user_account.balance,
                transaction_type=BORROWED,
            )

            borrowed_mail(
                user,
                book.price,
                'Borrow Message',
                'email_templates/borrowed_email.html',
                user_account.balance,
            )

            book.borrowers.add(user)
            borrowers_list.append(book)
            messages.success(request, 'Book borrowed successfully!')

    elif 'return' in request.POST:
        from django.utils import timezone
        from datetime import timedelta

        # Find the original 'BORROWED' transaction for this user and book
        borrow_transaction = Transaction.objects.filter(
            account=user_account,
            transaction_type=BORROWED
        ).order_by('-timestamp').first()

        late_fee = Decimal('0.00')
        if borrow_transaction:
            # Set loan period to 14 days (change as needed for testing)
            due_date = borrow_transaction.timestamp + timedelta(days=14)
            current_time = timezone.now()

            if current_time > due_date:
                overdue_days = (current_time - due_date).days
                if overdue_days < 1:
                    overdue_days = 1 # Minimum 1 day fine if past due

                # Charge $2.00 per overdue day
                late_fee = Decimal(str(overdue_days * 2.00))

        total_refund = Decimal(str(book.price)) - late_fee

        if total_refund < 0:
            total_refund = Decimal('0.00') # Prevent negative refunds if fine exceeds book price

        # Update user wallet balance
        user_account.balance += total_refund
        user_account.save()

        # Record the return transaction
        Transaction.objects.create(
            account=user_account,
            amount=total_refund,
            balance_after_transaction=user_account.balance,
            transaction_type=RETURN,
        )

        book.borrowers.remove(user)

        if late_fee > 0:
            messages.warning(request, f'Book returned late! A late fee of ${late_fee} was deducted from your refund.')
        else:
            messages.success(request, 'Book returned successfully with a full refund!')

    comments = models.Comment.objects.filter(book=book)
    comment_form = forms.CommentForm(initial={'user': user})

    return render(
        request,
        'book_detail.html',
        {
            'book': book,
            'comments': comments,
            'comment_form': comment_form,
        },
    )
@login_required
def toggle_wishlist(request, book_id):
    book = get_object_or_404(models.Book, id=book_id)
    wishlist_item, created = models.Wishlist.objects.get_or_create(user=request.user, book=book)

    if not created:
        wishlist_item.delete()
        messages.info(request, 'Removed from your wishlist.')
    else:
        messages.success(request, 'Added to your wishlist!')

    return redirect('book_detail', book_id=book.id)
@login_required
def wishlist_view(request):
    wishlist_items = models.Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})