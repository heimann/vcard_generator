# -*- coding: utf-8 -*-

import phonenumbers
import vobject
import base64
import codecs

print "Welcome to the vCard generator! All I need is some basic info and I'll\
 generate a vCard for you."
phone_number = raw_input("Phone number: ")
name = raw_input("Name: ")
email = raw_input("Email address: ")
image = None

image_boolean = raw_input("Do you have a JPG you would like to put in the card? (Yes or No): ")
if image_boolean.lower() == 'yes':
    while image_grab == True:
        image_input = raw_input("Name of the image (Make sure it's in the same directory as this script): ")
        try:
            logo = image_input
            f = open(logo, 'rb')
            image = f.read
            f.close()
            image_grab == False
        except:
            image_exception = raw_input("Hmm. Something went wrong, wanna try again? (Yes or No): ")
            if image_exception.lower() == True:
                image_grab == True
            else:
                image_grab == False



# Converts copilot numbers to twilio approved e164 format.
# Taken from Twilio's python integration.
def convert_to_e164(raw_phone):
   if not raw_phone:
       return

   if raw_phone[0] == '+':
       # Phone number may already be in E.164 format.
       parse_type = None
   else:
       # If no country code information present, assume it's a US number
       parse_type = "US"

   phone_representation = phonenumbers.parse(raw_phone, parse_type)
   return phonenumbers.format_number(phone_representation,
       phonenumbers.PhoneNumberFormat.E164)


file_name = convert_to_e164(phone_number)[1:] + '.vcf' # Removes the + so that they can be stored pure on AWS.

c = vobject.vCard()
c.add('n')
c.n.value = vobject.vcard.Name( given=name )
c.add('fn')
c.fn.value = name
c.add('email')
c.email.value = email
c.email.type_param = 'INTERNET'
c.add('tel')
c.tel.type_param = 'HOME'
c.tel.value = phone_number

# The photo is a little iffy I need to play around with this more.
# Seems to cause issues on some phones.
if image is not None:
    c.add('photo')
    c.photo.encoding_param = 'b'
    c.photo.type_param = 'JPEG'
    c.photo.value = image
output = c.serialize()

print c

with open(file_name, 'wt') as out:
   out.write(output)
   out.close()

print 'Yay! We done.'
