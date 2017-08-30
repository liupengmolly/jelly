from usst_info.settings import colleges,majors

def variables(request):
    return {'colleges':colleges,'majors':majors}
