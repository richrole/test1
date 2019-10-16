# python2 manage.py $ages
if ($args.count -eq 0) {
    python manage.py runserver
} else {
    python manage.py $args
}