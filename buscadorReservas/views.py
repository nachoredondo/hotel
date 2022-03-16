from django.conf import settings
from django.shortcuts import render
from buscadorReservas.models import Reservation, Room
from buscadorReservas.forms import FormContact, FormDateReservation, FormCreateReservation
from django.core.mail import send_mail
import datetime

# Create your views here.

def main(request):
    reservation = Reservation.objects.all()
    return render(request, "list_reservation.html", {"reservation": reservation})


# remove rooms reservated and data are formated
def room_not_reserved(room, rooms_reservated, n_days):
    room_not_reservated = []
    for r in room:
        if r.id not in rooms_reservated:
            r.price = r.price * n_days
            r.capacity = capacity(r.capacity)
            room_not_reservated.append(r)
    return room_not_reservated


def room_reservated(entry_date, departure_date):
    rooms_reservated = []
    
    # entry db between date form
    reservation = Reservation.objects.all().filter(entry_date__gt = entry_date).filter(entry_date__lt = departure_date)
    for res in reservation:
        rooms_reservated.append(res.room_id)
    # departure db between date form
    reservation = Reservation.objects.all().filter(departure_date__gt = entry_date).filter(departure_date__lt = departure_date)
    for res in reservation:
        rooms_reservated.append(res.room_id)
    # entry form between date db
    reservation = Reservation.objects.all().filter(entry_date__lt = entry_date).filter(departure_date__gt = entry_date)
    for res in reservation:
        rooms_reservated.append(res.room_id) 
    # departure form between date db
    reservation = Reservation.objects.all().filter(entry_date__lt = departure_date).filter(departure_date__gt = departure_date)
    for res in reservation:
        rooms_reservated.append(res.room_id)
            
    return set(rooms_reservated)


def capacity(capacity):
    if (capacity == 1):
        return "Individual"
    elif (capacity == 2):
        return "Doble"
    elif (capacity == 3):
        return "Triple"
    elif (capacity == 4):
        return "Cuádruple"
    else:
        return "Indefinida"


def select_date_room(request):
    if request.method == "POST":
        date_form = FormDateReservation(request.POST) 

        if date_form.is_valid():
            data = date_form.cleaned_data # data form
            entry_date = data['entry_date']
            departure_date = data['departure_date']

            # control_date(request, entry_date, departure_date)
            if (entry_date > departure_date): 
                date_form = FormDateReservation()
                return render(request, "search_reservation.html", {
                    "err":"La fecha de entrada no puede ser mayor a la fecha de salida"
                })
            
            # control if departure_date is later than the current year
            if (departure_date > datetime.date(2023, 1, 1)): 
                date_form = FormDateReservation()
                return render(request, "search_reservation.html", {
                    "err":"La fecha de salida no puede ser mayor al 01-01-2023"
                })

            room = Room.objects.all().order_by('price', 'name')
            rooms_reservated = room_reservated(entry_date, departure_date)
            n_days = (departure_date-entry_date).days
            room_not_reservated = room_not_reserved(room, rooms_reservated, n_days)
        
            return render(request, "select_room.html", {
                "entry_date": entry_date, 
                "departure_date": departure_date,
                "room": room_not_reservated,
                "n_days": n_days,
            })
    else:
        date_form = FormDateReservation()
    
    return render(request, "search_reservation.html", {"form":date_form})  


def create_reservation(request, id, entry_date, departure_date):
    if request.method == "POST":
        date_form = FormCreateReservation(request.POST) 
        if date_form.is_valid():
            post = date_form.cleaned_data # data form
            room = post['room']
            entry_date = post['entry_date']
            departure_date = post['departure_date']
            name = post['name']
            email = post['mail']
            phone_number = post['phone_number']
            n_guest = post['n_guest']

            # data room from db
            room_db = Room.objects.get(id=room)

            localizator = str(id) + room_db.name
            n_days = (departure_date-entry_date).days
            price = n_days * room_db.price
            type_room = capacity(room_db.capacity)
            
            # insert new reservation into db
            reservation = Reservation(
                entry_date=entry_date, 
                departure_date=departure_date, 
                room_id=room,
                n_guests=n_guest,
                name=name,
                mail=email,
                phone_number=phone_number,
                price=price,
                localizator=localizator)

            reservation.save()

            # send message with confirmation
            message = 'Hola ' + name + ',\n\n' 
            message += 'Acaba de ralizar correctamente la reserva para una habitación ' + type_room + ' en el hotel .'
            message += ' Con fecha de entrada ' + str(entry_date) + ' y fecha de salida  ' + str(departure_date) + '.'
            message += ' El número de localizador de la reserva es: ' + localizator + '.\n\n'
            message += 'Si tiene aluna duda no dude en preguntarnos.\n\n'
            message += 'Un saludo.'
            send_mail(
                'Reserva realizada-Chappsolutions',
                message,
                '',
                [email],
            )                 
            
            reservation = Reservation.objects.all()            
            return render(request, "list_reservation.html", {
                "reservation": reservation,
                "entry_date": entry_date, 
                "departure_date": departure_date,
                "room": room,
                "localizator": localizator,
            })
    else:
        date_form = FormCreateReservation()
    
    # data room from db
    room_db = Room.objects.get(id=id)
    type_room = capacity(room_db.capacity)
    entry_date = datetime.datetime.strptime(entry_date, "%Y-%m-%d")
    departure_date = datetime.datetime.strptime(departure_date, "%Y-%m-%d")
    n_days = (departure_date-entry_date).days
    return render(request, "create_reservation.html", {
        "id": id,
        "entry_date": entry_date,
        "departure_date": departure_date,
        "form":date_form,
        "capacity": type_room,
        "name_room": room_db.name,
        "price_total": n_days * room_db.price,
    }) 


def contact(request):
    if request.method == "POST":
        contact_form = FormContact(request.POST) 

        if contact_form.is_valid():
            data = contact_form.cleaned_data # data form
            email_host = settings.EMAIL_HOST_USER
            send_mail(
                data['asunto'],
                data['message'],
                '',
                [email_host],
            )
            return render(request, "email_sent.html")
    else:
        contact_form = FormContact()
    
    return render(request, "form_contact.html", {"form":contact_form}) 