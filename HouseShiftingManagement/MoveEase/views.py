from django.shortcuts import render
from twilio.rest import Client
import re
import datetime
from . models import User_Registration,Booking_detail,customers_review
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from redmail import gmail
from pytz import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
places = {
        "Chennai": [
            "Anna Nagar", "Adyar", "T. Nagar", "Mylapore", "Pallavaram", "Guindy","Nungambakkam", "Egmore", "Velachery", "Besant Nagar", "Kodambakkam",
            "Chromepet", "Mount Road", "Saidapet", "Thiruvanmiyur", "Ambattur","Porur", "Vadapalani", "Royapettah", "Mogappair", "Perambur",],
        "Madurai": [
            "KKNagar", "Melur", "Goripalayam", "Villapuram", "Anna Nagar","Tallakulam", "Simakkal", "Thirunagar", "Ellis Nagar", "Ponmeni",
            "Pasumalai", "Kochadai", "S S Colony", "Koodal Nagar",],
        "Bangalore": [
            "Koramangala", "Indiranagar", "Jayanagar", "Whitefield", "Electronic City","Marathahalli", "BTM Layout", "HSR Layout", "Bannerghatta Road",
            "Malleshwaram", "Basavanagudi", "Yelahanka", "Hebbal", "Banashankari","Rajajinagar", "Kengeri", "Cunningham Road", "J.P. Nagar", "R.T. Nagar","Bellandur",],
        "Mumbai": [
            "Andheri", "Bandra", "Colaba", "Dadar", "Juhu", "Malad", "Santacruz","Powai", "Worli", "Borivali", "Charni Road", "Goregaon", "Khar", "Navi Mumbai",
            "Vile Parle", "Thane", "Versova", "Chembur", "Kandivali", "Sion",],
        "Delhi": [
            "Connaught Place", "Karol Bagh", "Chanakyapuri", "Dwarka", "Lajpat Nagar","Paharganj", "Rajouri Garden", "Saket", "Vasant Kunj", "Greater Kailash",
            "Nehru Place", "Rohini", "Laxmi Nagar", "Pitampura", "Mayur Vihar","Shahdara", "Hauz Khas", "South Extension", "Malviya Nagar", "Kalkaji",
        ],
    }


def home(request):
    user = "Guest User"
    cus_review = customers_review.objects.all()
    return render(request,"home.html",{"user":user,"review":cus_review})


@csrf_exempt
def verify_login(request):
    global client,verified_number,verify_sid
    current_user_contact = None
    if request.method == "POST":
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        print(contact)
        if email != None:
            if User_Registration.objects.filter(email=email):
                current_user = User_Registration.objects.get(email=email)
                current_user_contact = current_user.contact
            else:
                return JsonResponse({"Error":"Email is not Registered"})
            
        if current_user_contact != None or contact != None:  
            account_sid = "ACea2f0739331d9e8d6e5ed08a8023f90e"
            auth_token = "05a0056c8cc35ebb856f1e7ab758b18b"
            verify_sid = "VA1a77818ed6ff07dfb9740f3975156e43"
            if contact != None:
                verified_number = "+91"+str(contact)
            else:
                verified_number = "+91"+str(current_user_contact)
            client = Client(account_sid, auth_token)
            verification = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=verified_number, channel="sms")
            print(verification.status)
            return JsonResponse({"Message":"OTP Send To the Mobile NUmber"})
        
@csrf_exempt
def user_registration(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        otp = request.POST.get("otp")
        print(otp)
        email_pattern =email_pattern = re.search(r"^[a-z0-9]+([\._]?[a-z0-9]+)*@[a-z]{5}+\.[a-z]{2,3}$",email)
        ph_num_pattern = re.match("^[6-9]{1}[0-9]{9}$",contact)
        password_pattern = re.search(r"^[a-z0-9]+[a-z0-9\W_]", password1)
        try:
            name = name.replace(" ","")
            if not name.isalpha():
                raise Exception("Name must be in Alphabets")
            elif len(name) == 0 or name.isspace():
                raise Exception("Name must Not be empty")
            elif len(name) <= 3:
                raise Exception("Please Enter The Valid Name")
            
            if len(email) == 0 or email.isspace():
                raise Exception("Email must not be empty")
            elif not email_pattern:
                raise Exception("Email should be in the correct pattern (Eg: dnagaraj3828@gmail.com)")
            
            if not contact.isdigit():
                raise Exception ("Phone Number must be in digits.")
            elif len(contact) != 10:
                raise Exception ("Phone Number must be 10 digits")
            elif not ph_num_pattern:
                raise Exception ("Phone Number must be starts with 6-9 and 10 digits(Eg:6379276534)")
            
            if len(password1) == 0 or password1.isspace():
                raise Exception("Password must not be empty")
            elif len(password2) == 0 or password2.isspace():
                raise Exception("confirm password must not br empty")
            elif len(password1) < 7 or len(password1) >20:
                raise Exception("Password length Should be in length of 7 to 20")
            elif not password_pattern:
                raise Exception("password should be in this format Eg:nagaraj@007")
            elif password2 != password1:
                raise Exception("Password and confirm password must be the same")
            
            if otp == "":
                raise Exception("Please Enter the Otp")
            elif not otp.isdigit():
                raise Exception ("Otp must be in digits.")
            elif len(otp) != 6:
                raise Exception("Please Enter the 6 digit OTP")
            else:
                if not User_Registration.objects.filter(email=email).exists():
                    verification_check = client.verify.v2.services(verify_sid) \
                    .verification_checks \
                    .create(to=verified_number, code=int(otp))
                    print(verification_check.status)

                    if verification_check.status == "approved":
                        my_data = User_Registration(name=name, email=email, contact=contact, password=password1)
                        my_data.save()
                        return JsonResponse({"message": "Registration successful"})
                    else:
                        return JsonResponse({"Error": "Wrong Otp"})
                else:
                    raise Exception("This Email is Already Exists")
        except Exception as er:
            error = str(er)
            return JsonResponse({"Error": error})

    return render(request, "home.html")

@csrf_exempt
def customer(request):
    current_user = User_Registration.objects.get(email=email)
    if request.method == "POST":
        city = request.POST.get('city_data')
        if city:
            localities = places.get(city, []) 
            return JsonResponse({"localities": localities})
    return render(request, "customer_app.html", {'user': current_user.name, 'places': places})

def inventry(request):
    current_user = User_Registration.objects.get(email=email)
    return render(request, "select_inventry.html",{'user': current_user.name})
                      
@csrf_exempt
def user_login(request):
    global email
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User_Registration.objects.filter(email=email).exists():
            current_user = User_Registration.objects.get(email=email)
            
            if password == current_user.password:
                user_data = {
                    "customer": (current_user.MoveEasePerson == False and current_user.delivery_person == False),
                    "move_ease_person": current_user.MoveEasePerson == True,
                    "delivery_person": current_user.delivery_person == True
                }
                return JsonResponse({"data_user": user_data})
            else:
                return JsonResponse({"Error": "password is incorrect"})
        else:
            return JsonResponse({"Error":"Email does not exist"}) 

@csrf_exempt
def forget_pass(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User_Registration.objects.filter(email=email).exists():
            password1= request.POST.get("password1")
            password2= request.POST.get("password2")
            password_pattern = re.search(r"^[a-z0-9]+[a-z0-9\W_]", password1)
            otp = request.POST.get("otp_forget")
            try:
                if len(password1) == 0 or password1.isspace():
                    raise Exception("Password must not be empty")
                elif len(password2) == 0 or password2.isspace():
                    raise Exception("confirm password must not br empty")
                elif len(password1) < 7 or len(password1) >20:
                    raise Exception("Password length Should be in length of 7 to 20")
                elif not password_pattern:
                    raise Exception("password should be in this format Eg:nagaraj@007")
                elif password2 != password1:
                    raise Exception("Password and confirm password must be the same")
                
                if otp == "":
                    raise Exception("Please Enter the Otp")
                elif not otp.isdigit():
                    raise Exception ("Otp must be in digits.")
                elif len(otp) != 6:
                    raise Exception("Please Enter the 6 digit OTP")
                else:
                    verification_check = client.verify.v2.services(verify_sid) \
                    .verification_checks \
                    .create(to=verified_number, code=int(otp))
                    print(verification_check.status)
                    if verification_check.status == "approved":
                        User_Registration.objects.filter(email=email).update(password=password1)
                        return JsonResponse({"message": "Password Updated Successfully"})
                    else:
                        raise Exception("Incorrect OTP")
            except Exception as er:
                return JsonResponse({"Error":str(er)})
                
        else:
            return JsonResponse({"Error":"Email does not exist"})

@csrf_exempt
def map(request):
    global start_location,end_location,distance_km
    if request.method == "POST":
        start_location = request.POST.get("from_location")
        end_location = request.POST.get("to_location")
        city = request.POST.get("city")
        shifted_from = request.POST.get("shift_from")
        shifted_to = request.POST.get("shift_to")
         
        if city != None:
            try:
                if city != "":
                    if shifted_from == shifted_to:
                        raise Exception("The Shifting from and shisting location to must not be the same")
                    else:
                        start_location = shifted_from +","+ city
                        end_location = shifted_to +","+ city
                else:
                    raise Exception("Please Select The City")
            except Exception as er:
                CityError = str(er)
                return JsonResponse({"Error": CityError})
        
        if  start_location != None:
            try:
                if start_location == "" or start_location.isspace():
                    raise Exception("Shifting From Location must not be Empty")
                elif len(start_location) <= 3:
                    raise Exception("Please Enter the Valid Shifthing from Location")
                if end_location == "" or end_location.isspace():
                    raise Exception("Shifting To Location must not be Empty")
                elif len(end_location) <= 3:
                    raise Exception("Please Enter the Valid Shifthing To Location")
                if start_location == end_location:
                    raise Exception("Shifthing From and Shifthing To Location must not be same")
            except Exception as er:
                LocationError = str(er)
                return JsonResponse({"LocationError": LocationError})
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            starting_location = geolocator.geocode(start_location)
            ending_location = geolocator.geocode(end_location)
            
            if starting_location and ending_location:
                start_coords = (starting_location.latitude, starting_location.longitude)
                end_coords = (ending_location.latitude, ending_location.longitude)
                
                distance_km = geodesic(start_coords, end_coords).kilometers
                print(distance_km)

                return JsonResponse({"message":"success"})
            else:
                return JsonResponse({"LocationError": "Please check your place names are valid."})

        except Exception as er:
            return JsonResponse({"LocationError": str(er)})

def free_qoute(request):
    current_user = User_Registration.objects.get(email=email)
    return render(request,"free_quote.html",{"user": current_user.name})


@csrf_exempt
def send_quotation(request):
    current_user = User_Registration.objects.get(email=email)
    get_email = current_user.email
    name = current_user.name
    price = 0
    if request.method == 'POST':
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        house = request.POST.get('house')
        try:
            if from_location == "" or from_location.isspace():
                raise Exception("Shifting From Location must not be Empty")
            elif len(from_location) <= 3:
                raise Exception("Please Enter the Valid Shifthing from Location")
            if to_location == "" or to_location.isspace():
                raise Exception("Shifting To Location must not be Empty")
            elif len(to_location) <= 3:
                raise Exception("Please Enter the Valid Shifthing To Location")
            
            if from_location == to_location:
                raise Exception("Shifthing From and Shifthing To Location must not be same")
            else:
                if house == '1bhk':
                    price = 10000.00
                elif house == '2bhk':
                    price = 15000.00
                elif house == '3bhk':
                    price = 20000.00
                gmail.username="moveease89@gmail.com"
                gmail.password="bmbx vjos hmli wppd"
                gmail.send(
                    subject=f'Quotation for {name}',
                    receivers=get_email,
                    html=f"""<html>
                                <body>
                                    <p>Dear {name},</p>
                                    
                                    <p>Thank you for requesting a quotation for your house shifting.</p>
                                    
                                    <table style="width:100%;" border="2px solid black">
                                        <tr>
                                            <th>Field</th>
                                            <th>Details</th>
                                        </tr>
                                        <tr>
                                            <td>Shifted From</td>
                                            <td>{from_location}</td>
                                        </tr>
                                        <tr>
                                            <td>Shifted To</td>
                                            <td>{to_location}</td>
                                        </tr>
                                        <tr>
                                            <td>House Type</td>
                                            <td>{house}</td>
                                        </tr>
                                    </table>
                                    
                                    <p>Total Cost: {price} </p>

                                    <p>If you have any further questions or would like to proceed, please feel free to contact us at moveeaseadmin@gmail.com</p>
                                    
                                    <p>Best regards,<br>MoveEaseAdmin Team</p>
                                </body>
                            </html>""")
                return JsonResponse({"message":'Quotation sent successfully'})
            
        except Exception as er:
            return JsonResponse({"Error": str(er)})
        
    

@csrf_exempt
def payment_receipts(request):
    global bhktype,correct_time,cortons,vechile,total_price
    Error = ""
    total_price = 0
    delivery_charges = 10000
    per_km_price = 30
    total_km_price = 0
    bhk_price = 0
    cortons_price = 0
    single_cortans_price = 60
    if request.method == "POST":
        bhktype = request.POST.get('type')
        time_str = request.POST.get('time') 
        cortons = request.POST.get('cortons')
        vechile = request.POST.get('vechile')
        try:
            if bhktype == '1BHK':
                bhk_price = 10000
            elif bhktype == '2BHK':
                bhk_price = 15000
            elif bhktype == '3BHK':
                bhk_price = 20000
            elif bhktype is None or bhktype == "":
                raise Exception("Please select a BHK type")

            if time_str is None or time_str == "":
                raise Exception("Please select a time")
            
            time = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
            
            if time < datetime.datetime.now():
                raise Exception("Please select a different time")
            
            correct_time = time.replace(tzinfo=timezone('UTC'))

            if cortons:
               cortons_price = (int(cortons) * single_cortans_price) 

            if vechile == "Tata 407":
                vechiles_price = 6900
            elif vechile == "Dost":
                vechiles_price = 6100
            elif vechile == "Eicher Truck":
                vechiles_price = 9000
            elif vechile == "Tata Truck":
                vechiles_price = 15900
            elif vechile is None or vechile == "":
                raise Exception("Please select a vechile")
            total_km_price = (distance_km * per_km_price)
            
            total_price = vechiles_price + total_km_price + cortons_price + bhk_price + delivery_charges
            
            pay_when_delivered = total_price-(total_price*(20/100))
            booking_amount = total_price*(20/100)
            
            context = {"total_price": total_price, "from_location": start_location, "to_location": end_location,
                       "vechiles_price":vechiles_price, "bhk_price":bhk_price,"delivery_price":delivery_charges,
                       "cortons_price":cortons_price,"total_km_price":total_km_price,"message":"success",
                       "booking_amount":booking_amount,"pay_when_delivered":pay_when_delivered}
            return JsonResponse(context)
        except Exception as er:
            
            Error = str(er)
            return JsonResponse({"Error": Error})
        
def payment(request):
    current_user = User_Registration.objects.get(email=email)
    return render(request, "payment.html",{"user":current_user.name})


def is_valid_date(date_string):
    try:
        datetime.datetime.strptime(date_string,"%m/%Y")
        return True
    except ValueError:
        return False


@csrf_exempt
def save_bookings(request):
    if request.method == "POST":
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        upi_number = request.POST.get("upi_number")
        upi_pin = request.POST.get("upi_pin")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if upi_number == None and username == None:
            try:
                card_number = card_number.replace(" ", "")
                if card_number == "":
                    raise Exception("Card number must not be empty")
                elif not card_number.isdigit():
                    raise Exception("Card number must be a number")
                elif len(card_number) != 16:
                    raise Exception("Invalid card number")
                
                current_date = datetime.date.today()
                expiration_date_pattern = datetime.datetime.strptime(expiry_date,"%m/%Y")
                expiration_month = expiration_date_pattern.month
                expiration_year = expiration_date_pattern.year
                expiration_start_date = datetime.datetime(expiration_year, expiration_month, 1).date()
                valid_years = range(2023, 2031)

                if not is_valid_date(expiry_date):
                    raise Exception ("\nExpire Date should be in this format (Eg:12/2023)")
                elif expiration_start_date < current_date:
                    raise Exception ("Card has expired,please update to current year {}.".format(current_date.year))
                elif expiration_year not in valid_years:
                    raise Exception ("Invalid expiration year.Please enter a date between 2023 and 2030.")

                if not cvv.isdigit():
                    raise Exception ("CVV must be a Number.")
                elif len(cvv) == 0 or cvv.isspace():
                    raise Exception ("CVV should not be empty.")
                elif len(cvv) != 3:
                    raise Exception ("Please Enter the correct CVV")
                
            except Exception as er:
                CardError = str(er)
                return JsonResponse({"cardError":CardError})
            
        elif card_number == None and username == None:
            try:
                ph_num_pattern = re.match("^[6-9]{1}[0-9]{9}$",upi_number)
                if not upi_number.isdigit():
                    raise Exception ("Phone Number must be in digits.")
                elif len(upi_number) != 10:
                    raise Exception ("Phone Number must be 10 digits")
                elif not ph_num_pattern:
                    raise Exception ("Phone Number must be starts with 6-9 and 10 digits(Eg:6379276534)")
                
                upi_pin = str(upi_pin)
                

                if not upi_pin.isdigit():
                    raise Exception ("PIN must be a Number.")
                elif len(upi_pin) == 0 or upi_pin.isspace():
                    raise Exception ("PIN should not be empty.")
                elif len(upi_pin) not in (4,6):
                    raise Exception ("PIN should be in the length of 4 or 6.")
            except Exception as er:
                
                upi_Error = str(er)
                return JsonResponse({"upi_Error": upi_Error})
            
        elif card_number == None and upi_number == None:
            try:
                net_id_pattern = re.search(r"^[a-z]{3,10}+[0-9]{2,6}$",username)
                if len(username) < 5 or len(username) > 20:
                    raise Exception ("User Id should be in the length of 5 to 20 charcters.")
                elif not net_id_pattern:
                    raise Exception ("User Id should be 3 small character and atleast 2 numbers and in this Format (Eg:john123)")

                if password.isspace():
                    raise Exception ("Password Shold not be Empty")
                elif len(password) < 3 or len(password) > 20:
                    raise Exception ("Password should be in the length of 3 to 20")
            except Exception as er:
                
                netError = str(er)
                return JsonResponse({"netError": netError})
            
        if card_number or upi_number or username:
            current_user = User_Registration.objects.get(email=email)
            book_detail = Booking_detail(user=current_user,email=current_user.email,shifting_from=start_location,
                                         shifting_to=end_location,bhk_type=bhktype,service_time=correct_time,
                                         extra_cortans=cortons,selected_vehicle=vechile,bill_amount=total_price)
            book_detail.save()
            return JsonResponse({"Booking_detail":"Booking_success"})

            
def my_booking(request):
    current_user = User_Registration.objects.get(email=email)
    current_booking = Booking_detail.objects.filter(email=current_user.email,deliver_status=True,payment_status=False)
    booking_history = Booking_detail.objects.filter(email=current_user.email,deliver_status=True,payment_status=True)
    context = {"user":current_user.name,"current_booking":current_booking,"Booking_history":booking_history}
    return render(request,"my_booking.html",context)

@csrf_exempt
def delete_booking_detail(request):
    if request.method == "POST":
        id = request.POST.get("bookid")
        book = Booking_detail.objects.get(id=id)
        book.delete()
        return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":0})
    
def move_ease_app(request):
    current_booking = Booking_detail.objects.filter(deliver_status=False)
    delivery_person = User_Registration.objects.filter(delivery_person=True)
    booking_history = Booking_detail.objects.filter(deliver_status=True,payment_status=True)
    return render(request,"move_ease_app.html",{'current_booking':current_booking,"delivery_person":delivery_person,"Booking_history":booking_history})

def delivery_person_app(request):
    work_assign = Booking_detail.objects.filter(deliver_status=True, delivery_person=email)
    return render(request,"delivery_app.html",{'word_assign':work_assign})

def user_profile(request):
    current_user = User_Registration.objects.get(email=email)
    user = User_Registration.objects.filter(email=email)
    return render(request,"profile_setting.html",{"user":current_user.name,"User_data":user})

    
@csrf_exempt
def update_booking_detail(request):
    if request.method == "POST":
        id = request.POST.get("bookid")
        delivery_person = request.POST.get("delivery_person")
        if delivery_person != None:
            Booking_detail.objects.filter(id=id).update(deliver_status=True,delivery_person=delivery_person)
        else:
            Booking_detail.objects.filter(id=id).update(payment_status=True)
        return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":0})
    
@csrf_exempt
def update_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        up_email = request.POST.get("email")
        contact = request.POST.get("contact")
        email_pattern = re.search(r"^[a-z0-9]+([\._]?[a-z0-9]+)*@[a-z]{5}+\.[a-z]{2,3}$",up_email)
        ph_num_pattern = re.match("^[6-9]{1}[0-9]{9}$",contact)
        
        try:
            if not name.isalpha():
                raise Exception("Name must be in Alphabets")
            elif len(name) == 0 or name.isspace():
                raise Exception("Name must Not be empty")
            elif len(name) <= 3:
                raise Exception("Please Enter The Valid Name")
            
            if len(up_email) == 0 or up_email.isspace():
                raise Exception("Email must not be empty")
             
            elif not email_pattern:
                raise Exception("Email should be in the correct pattern (Eg: dnagaraj3828@gmail.com)")
            
            if not contact.isdigit():
                raise Exception ("Phone Number must be in digits.")
            elif len(contact) != 10:
                raise Exception ("Phone Number must be 10 digits")
            elif not ph_num_pattern:
                raise Exception ("Phone Number must be starts with 6-9 and 10 digits(Eg:6379276534)")
            if email != up_email:
                if User_Registration.objects.filter(email=up_email).exists():
                    raise Exception("This Email is already registered")
            
            User_Registration.objects.filter(email=email).update(name=name,email=up_email,contact=contact)
            return JsonResponse({"message":"User Updated Successfully"})
            
        except Exception as er:
            
            error = str(er)
            return JsonResponse({"error": error})
        
@csrf_exempt
def change_password(request):
    if request.method == "POST":
        curpass = request.POST.get("curpass")
        if User_Registration.objects.filter(password=curpass).exists():
            password1= request.POST.get("password1")
            password2= request.POST.get("password2")
            password_pattern = re.search(r"^[a-z0-9]+[a-z0-9\W_]", password1)
            try:
                if password1 == "" or password1.isspace():
                    raise Exception("Password must not be empty")
                elif password2 == "" or password2.isspace():
                    raise Exception("Confirm Password must not be empty")
                elif len(password1) < 7 or len(password1) >20:
                    raise Exception("Password length Should be in length of 7 to 20")
                elif not password_pattern:
                    raise Exception("password should be in this format Eg:nagaraj@007")
                elif password2 != password1:
                    raise Exception("Password and confirm password must be the same")
                

                if password1 == password2:
                    User_Registration.objects.filter(email=email).update(password=password1)
                    return JsonResponse({"message":"Password Updated Successfully"})
                
            except Exception as er:

                return JsonResponse({"error": str(er)})
        else:
            return JsonResponse({"error": "Invalid Current password"})
                
    
@csrf_exempt
def add_delivery_person(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        delivery = request.POST.get("delivery_person")
        email_pattern =email_pattern = re.search(r"^[a-z0-9]+([\._]?[a-z0-9]+)*@[a-z]{5}+\.[a-z]{2,3}$",email)
        ph_num_pattern = re.match("^[6-9]{1}[0-9]{9}$",contact)
        password_pattern = re.search(r"^[a-z0-9]+[a-z0-9\W_]", password1)
        try:
            if not name.isalpha():
                raise Exception("Name must be in Alphabets")
            elif len(name) == 0 or name.isspace():
                raise Exception("Name must Not be empty")
            elif len(name) <= 3:
                raise Exception("Please Enter The Valid Name")
            
            if len(email) == 0 or email.isspace():
                raise Exception("Email must not be empty")
            elif not email_pattern:
                raise Exception("Email should be in the correct pattern (Eg: dnagaraj3828@gmail.com)")
            if len(password1) == 0 or password1.isspace():
                raise Exception("Password must not be empty")
            elif len(password2) == 0 or password2.isspace():
                raise Exception("confirm password must not br empty")
            elif len(password1) < 7 or len(password1) >20:
                raise Exception("Password length Should be in length of 7 to 20")
            elif not password_pattern:
                raise Exception("password should be in this format Eg:nagaraj@007")
            elif password2 != password1:
                raise Exception("Password and confirm password must be the same")
            
            if not contact.isdigit():
                raise Exception ("Phone Number must be in digits.")
            elif len(contact) != 10:
                raise Exception ("Phone Number must be 10 digits")
            elif not ph_num_pattern:
                raise Exception ("Phone Number must be starts with 6-9 and 10 digits(Eg:6379276534)")
            
            
            if not User_Registration.objects.filter(email=email).exists():
                my_data = User_Registration(name=name, email=email, contact=contact, password=password1,delivery_person=delivery)
                my_data.save()
                return JsonResponse({"message": "Delivery Person Added successful"})
            else:
                raise Exception("This Email is Already Exists")
        except Exception as er:
            error = str(er)
            return JsonResponse({"Error": error})



