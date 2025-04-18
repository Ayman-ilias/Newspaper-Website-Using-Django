# Newspaper Website Using Django

A Django-based web application for managing and displaying news articles in a newspaper website. This project includes functionalities like displaying articles, managing posts, and an editorial section for content management.

## Features

- **User Authentication**: Users can sign up, log in, and log out.
- **News Articles**: View articles on various topics.
- **Editorial Access**: Editors can create, update, or delete posts.
- **CRUD Functionality**: For managing news posts.
- **Responsive Design**: Built with Bootstrap to ensure mobile responsiveness.

## Installation

To run this project locally, follow these steps:

1. Clone this repository:
   git clone https://github.com/Ayman-ilias/Newspaper-Website-Using-Django.git

2. Navigate to the project folder:
   cd Newspaper-Website-Using-Django

3. Set up a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install dependencies:
   pip install -r requirements.txt

5. Run database migrations:
   python manage.py migrate

6. Start the development server:
   python manage.py runserver

7. Visit http://127.0.0.1:8000/ in your browser to access the site.

## Editorial Login

To log in as an editor:
- **Username**: `msi99`
- **Password**: `1234`

## Usage

- Create, update, and delete news articles.
- Manage the content and ensure articles' accuracy.

## Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit the changes (`git commit -am 'Add new feature'`).
5. Push to your fork (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License.
