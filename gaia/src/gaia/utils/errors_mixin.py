from gaia.error import GaiaErrors

class ErrorsMixin:
    ' provide support to collect errors '

    def __init__(self):
        self.reset_errors()

    def reset_errors(self):
        self._collected_errors = []

    def add_error(self, e):
        self._collected_errors.append(e)

    def raise_if_errors(self):
        if self._collected_errors:
            raise GaiaErrors(*self._collected_errors)

    def errors(self):
        if self._collected_errors:
            return GaiaErrors(*self._collected_errors)
        else:
            return None
