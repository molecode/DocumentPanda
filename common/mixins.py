class FormViewW3Mixin(object):
    def get_form(self, form_class=None):
        form = super(FormViewW3Mixin, self).get_form(form_class)
        for _, form_field in form.fields.items():
            form_field.widget.attrs = {'class': 'w3-input w3-border'}
        return form
