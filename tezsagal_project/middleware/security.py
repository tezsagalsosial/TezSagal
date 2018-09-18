class ChangeHeader:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Set-Cookie'] = "PHPSESSID=9su3mfn95fshl9f02mt1p6s2f5; path=/; HttpOnly"
        response['x-xss-protection'] = 0
        response['status'] = 200
        response['X-Powered-By'] = 'PHP/7.1.8'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Strict-Transport-Security'] = 'max-age=8640000000'
        return response