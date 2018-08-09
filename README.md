This is Edward Kang's Final Project.

This is a web allows users to login, logout, select location, dates for the list, search cars with keyword, see detail information, and rent a car.

Superuser account
- username: admin
- Email: admin@example.com
- password: summer18

README.md
- Include a short writeup describing the project, what's contained in each file.

myIndex.js
- Contains all JS codes.

style.css
- It is css file for basic design of this website.

forms.py
- Extension of UserCreationForm that requires users to input their first name, last name and email address when they sign up.

views.py
- It is backend side codes.
- It checks user status like logged in status, whether superuser or not.
- It contains most functions this website uses.
- It renders webpages or send HttpResposne, JsonReponse back to webpages.
- It create, update db objects, pass results of queries.

layout.html
- It contains common features of websites like title, welcome text, displaying username, logout button, link to admin pages.
- It calls bootstrap, local css, external js file.
- It calls title and body blocks.
- When a user clicks title, 'Edward Kang's Final Project!', if a user is logged in, it redirects a user to main page.
- If not, it redirects a user to login page.

menu.html
- This time, created separate menu section as an html file so do not need to put same code for menu sectino for all other html files.

login.html
- A user can input username and password to login to the website.
- If a user types wrong username/password combination, display error message.
- Click sign up button allows a user to go to sign up page.
- If input username/password exist, redirects to main page.
- If user logged out, redirect to this page and display a message.

sign up.html
- A user can create new account.
- it displays an error message depends on situation liek too simple password, already exist, two passwords does not match.

error.html
- This page displays error messages with back button which redirects users to the previous page.
- If users try to access to other users reservation page, it displays an error message says they do not have an access to the page.
- If users try to make an reservation certain car for certain date range that is already booked, it displays an error message says it is not available for the selected date.
- If users try to pass invalid input as a parameter in URL, it displays an error message syas no result.

index.html
- It is main page, when user first logged in, directs to here.
- Users can select location of cars and select if they are under 25 or over 25 (which will affect on final price), and rental date range to see a list of available cars.
- Date range is required information so if user do not select it, it will alret message and make users to select date again.
- Selecting past date is unavailable.

search.html
- It contains a list of cars that matches with what users input.
- From here, user can enter keyword for brand, model, or type of cars which will retrieve cars meet the condition among the current list.
- Users can select to options like ascending, descending price or size of cars which will reorder the list.
- If users click view deal button of the car, redirects them to reservation page with detail information.

reservation.html
- It will display detail information of the selected car.
- It will display selected date range to remind the user.
- Users can select their prefer drop-off location which will change the location information of the car after the reservation is completed.
- Users can select the option to choose protection which cost $10 per day.
- If user selects yes, display extra protection cost next to it.
- On the bottom of the page, it will display total cost of the car exclude protection cost.
- If users selected under 25 option at the beginning, there will be young renter fee.
- If users click book now buttom, it will create new reservation.

history.html
- It contains a list of reservation the user made.
- The list contains car, date range, pick-off and drop-off locations, its total price, and the status of the reservation.
- If users click view reservation button of the reservation, redirects them to history detail page with detail information.

history detail.html
- Users can see information about the selected reservation.
- If users want to request cancellation for the reservation, they can select reservation cancel button.
- If users select the button, it pops out the modal and ask users one more time.
- If users select to confirm, the request get created that admin can approve or deny.
- Once the request get created, users can see new section which displays about the status of the request of the reservation.

admin reservation.html
- Admin can see the list of reservations.
- There are past, waiting, checked-in, and complete so admin can select the kind of reservations they want.

admin reservation detail.html
- If the reservation status is waiting, they can change it to checked-in status which means customer checked-in the car.
- If the reservation status is checked-in, they can change it to complete status which means customer returned the car.
- If the customer selected different location as an drop-off option, it will update location of the car.
- If there is a request for the reservation, it will display status of request with the link which redirects admin to the request page.

admin request.html
- Admin can see the list of requests.
- There are past, waiting, declined, and approved so admin can select the kind of requests they want.

admin request detail.html
- If admin approve the request, the reservation status will be changed to canceled, other customers will be able to see the car from the list again and request status get updated as approved.
- If admin decline the request, the reservation will remain same and request status get updated as declined.

Data structure
- User: user information with first name, last name, email address
- Locations: list of locations with its name and address
- Car: list of cars with brand, name, etc
- Reservation: list of reservations that will be created one a user select a certain car for certain date. Its status and request status will be updated for certain actions.
- ReservedDate: list of reserved date for certain cars which will be used to filter cars to check if the car is already reserved for selected date range. If it does, the list of cars willk not include the car reserved.
- Request: list of requests that will be created when users request to cancel the reservation. Its status and approval status shows what kind of request it is and if the reqeust is approved or not.

Student Comment
- Originally, I planned to implement Google Map features to display avaiable rental locations but faced the marking issue, so could not implemented.
- Another plan was implementing chat service, was working on it using django socketio, but could not finish on time also.
- Beside these, succesfully implemented features I proposed.
- Also implemented search features Alex suggested which allows users to search certain brand, name, or type of cars.
- Tried to steamline the code by using same function in JS for multiple features, introducing menu.html so do not repeat same code for menu sections for multiple html files, and using one html file to display several different type of results unlike the previous project.
- Want to improve this project by implementing chat service, APIs for map, credit card information, etc.
- I enjoyed this class, thank you.