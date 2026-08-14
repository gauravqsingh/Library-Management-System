# Library Management System

![Live Deployment](https://img.shields.io/badge/Render-Deployed-success?style=for-the-badge&logo=render)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

**Live Demo:** [https://library-management-system-ujoc.onrender.com](https://library-management-system-ujoc.onrender.com)

A robust, cloud-native full-stack web application designed to manage comprehensive library catalogs, dynamic book inventories, and user transactions.

This project was architected and developed collaboratively by **Gaurav Singh** and **Radhika Agarwal**.

## Key Features
- **User Authentication:** Secure registration, login, and profile management systems.
- **Dynamic Cataloging:** Borrow, return, and track books with real-time inventory updates.
- **Transaction History:** Dedicated dashboards for users to track their borrowing history.
- **Cloud Media Storage:** Integrated with **Cloudinary** for persistent, scalable hosting of dynamic media files (e.g., user-uploaded book covers).
- **Production-Ready Hosting:** Fully deployed on **Render** utilizing a Gunicorn web server and WhiteNoise for optimized static file delivery.
- **Automated Deployments:** Continuous integration pipeline linked via GitHub with automated database migrations and superuser provisioning.

## Technology Stack
- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Cloud Storage:** Cloudinary API
- **Deployment:** Render, Gunicorn, WhiteNoise, Bash (`build.sh`)

---
