# MoveEase: Smart Home Shifting

## Objective

Shifting to a new house is a time-consuming and challenging process. The goal of the "MoveEase" application is to provide a house shifting process management system that makes the entire process organized and hassle-free.

## Flow Of MoveEase

It seems like you're expanding the features of your "MoveEase: Smart Home Shifting" project to include more functionality related to the customer module. Here's an outline of the additional features you want to include:

### Customer Module (Enhanced)

1. **User Registration**:
   - Customers can register an account with their personal information, including name, contact details, and address.

2. **User Profile**:
   - Customers can log in to their accounts to view and manage their profile information.

3. **Free Quote Request**:
   - Customers can request a quote for the house shifting process by providing details such as the current location, destination, number of rooms, and the type of items to be transported.

4. **Customer Login**:
   - Registered customers can log in to their accounts to access the system.

5. **Select Inventory**:
   - Customers can select and manage the inventory of items to be transported, specifying details about each item.

6. **Invoice Generation**:
  - The module generates invoices for customers based on the quote and the services provided during the house shifting process.

7. **Payment Process**:
   - Customers can complete the payment process using multiple options, including credit/debit cards, cash, online transfers, and more.
      
8. **View Current Booking**:
   - Customers can view the details of their current bookings, including scheduled dates, item lists, and payment information.

9. **Track Current Booking**:
   - Customers can track the status and progress of their ongoing house shifting bookings, including the location of their items in transit.

10. **View Booking History**:
   - Customers can access their booking history to review past house shifting bookings, including details and payment records.
     
### Admin Module (Enhanced)

1. **Add Delivery Person**:
   - Admin users can add and manage delivery personnel by entering their details, such as name, contact information, and availability.

2. **View Current Bookings of the Customer**:
   - Admin users can view a list of current bookings made by customers, including details about the booking, customer information, and the status of the booking.

3. **Assign Work to Particular Delivery Persons**:
   - Admin users can assign specific bookings to delivery personnel based on their availability and location. This feature ensures efficient routing and assignment of delivery tasks.

### Delivery Person Module

1. **Login for Delivery Personnel**:
   - Delivery personnel can log in to their accounts to access the system.

2. **View Assigned Deliveries**:
   - Delivery personnel can view a list of deliveries assigned to them, including details about the customer, delivery address, and package contents.

3. **Update Delivery Status**:
   - Delivery personnel can update the status of each delivery, indicating whether it's in progress, completed, or if any issues have arisen.

## Used Apis
    1. **Twilio API**: It is used for SMS and phone call functionality. You can send SMS messages and make phone calls programmatically using the Twilio API.
    
    2. **Geopy API**: Geopy is a Python library that provides geocoding (converting an address into geographic coordinates) and distance calculation services. It is used to perform geocoding and calculate distances, which can be useful for location-based features in your application.
    
    3. **Redmail (Custom)**: The code mentions "redmail" for sending emails. However, "redmail" is not a widely known or standard Python package. It could be a custom package or module specific to your project. You may need to refer to your project's documentation or source code to understand how "redmail" is implemented and how to install it.
    
    In summary, you need to install Django, Twilio, and geopy using the provided installation commands. For "redmail," you should refer to your project's documentation or source code to determine how to install and use it, as it appears to be a custom component.

## Used Google Api for Map Generation when you click the Track Now Option.

1. **Get Google Maps API Key**:
   - You'll need to sign up for the Google Maps API and obtain an API key. This key will be used to authenticate your application when making requests to the Google Maps API.

2. **Integrate the API**:
   - Add the Google Maps JavaScript API to your project. You can do this by including the API script in your HTML templates. Here's an example of how to include it:

   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap" async defer></script>
   ```

   Replace `YOUR_API_KEY` with the actual API key you obtained.

3. **Create Maps**:
   - You can create interactive maps by using JavaScript to initialize the map, set markers, and add other elements like directions, overlays, and custom markers.

## Used the OpenCage Geocoding API for auto-suggestions.

1. **Sign Up and Get an API Key**:
   - Start by signing up for an OpenCage Data API account to obtain an API key. This key will be used to authenticate your application when making requests to the OpenCage API.

2. **API Request**:
   - In your code, you can make HTTP requests to the OpenCage Geocoding API endpoint, typically in the form of a GET request. Include your API key in the request URL as a query parameter.

3. **Auto-Suggestions**:
   - When users type into location input fields, you can send partial queries to the OpenCage API, which will provide auto-suggestions based on the user's input. The API will return a list of possible locations that match the input.

## Getting Started

To run this project locally, follow these steps:

1. Clone the repository to your local machine.

```bash
git clone https://github.com/yourusername/task-manager.git 
```
(or) Download the Project Folder in rar type and Extract it.

1.1. Open VSCode and Open the Project Folder . In VSCode Open Settings.py

Add this things in this settings.py

*In Database - 'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': ' ', 'USER':' ', 'PASSWORD':' ', 'HOST':'<'your localhost'> ', 'PORT':''}
Use Your Database details or use default sqllite3 database

```bash
pip install pymysql
```
#for creating model as Existing Table

2. Install the required dependencies using pip:

```bash
pip install Django
pip install twilio
pip install geopy
```
and all required pip install.

3. Create a database and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Access the application in your web browser at [http://localhost:8000](http://localhost:8000).

## Important Points

1. Exception Handling: The system should gracefully handle errors using exception handling.
2. Validations: Implement necessary validations to ensure data integrity and security.
3. UI and Designs: Create a rich user interface with well-thought-out designs.
4. Ajax and JQuery: Utilize Ajax and JQuery for smooth and responsive user interactions.
---
