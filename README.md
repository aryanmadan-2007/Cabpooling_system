The data is saved after every change
cab can leave with 1-2 students with no error
even if there are no cabs, it would just mean that we cannot dispatch any more cabs. requests would still be saved.
if two students are in the same year, it is compared by submitted_at time using heap function.


run program by the following command 
python.exe main.py

cab file format: [ { "driver_name": , "seats": , "destination": , "time_slot": , "has_left": , "students": } ]
