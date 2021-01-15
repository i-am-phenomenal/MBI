Clone the project using the following command
    ## git clone https://github.com/i-am-phenomenal/MBI.git

Navigate to the root directory of the project and run the following commands in order
    1) python manage.py makemigrations
    2) python manage.py migrate
    3) python manage.py runserver

This project was made using Python 3.7 and Django version 3.1.4 so please ensure that you have the required versions installed. 

The project structure consists of a backend folder (which is the app folder for django) and the mbi folder (which containsn config related details and urls)

Currently, the stripe credentials are hardcoded in the settings.py file and can be used for testing purposes.

NOTE: Once you are logged in and you are asked to enter your card credentials, this stripe account accepts only Visa and mastercard account card numbers. Otherwise all the other numbers woukd be deemed invalid. 
Some examples of successful card numbers can be found here https://stripe.com/docs/testing


Schema's used in this project are 
Manager -> 
    id
    emailId
    firstName
    lastName
    dateofBirth
    company
    cardDetails (ForeignKey to PaymentMethod resource)
    isAdmin 
    isStaff
    isActive
    isSuperuser
    insertedAt
    updatedAt

USERNAME FIELD -> emailId
REQUIRED FIELDS -> password, company, dateOfBirth

PaymentMethod ->
    id
    type
    cardNumber
    expiryMonth
    expiryYear
    cvv
    insertedAt
    updatedAt    

Product -> 
    id
    productName
    insertedAt
    updatedAt

Price -> 
    id
    product (ForeignKey to Product resource)
    currency
    unitAmount
    billingScheme
    interval
    intervalCount
    insertedAt
    updatedAt

Subscription -> 
    id
    customer (ForeignKey to Manager resource)
    price (ForeignKey to Price resource)
    insertedAt
    updatedAt

TYPICAL FLOW

Sign up -> Login -> Dashboard

Once the user is on the dashboard
The user can see the subscriptions they have subscrbed to from the left side panel
If there are no subscriptions, they would be prompted to click on a button from where they can see the available subscriptions to subscribe to. All the plans are monthly and the products were created on the stripe website account first. You can also create a product using the POST (product/create/) API. See the @validateIfProductNamePresent decorator to check which fields are necessary
Once they click on subscribe, they will see an alert upon success. 
Then on the same left panel, they can see the plans they have subscribed to.
They can either unsubscribe from the plan or they can pay for the plan by clicking on the respective icons. 
Before Subscribing to a plan, the user needs to enter their card details from the dashboard which they can remove. 


NOTE: Since both the frontend and the backend projects are separately written, please make sure that you have both the projects running on different Terminals/Command Prompts. Also ensure that react project is running on Port 3000 and Django project on Port 8000