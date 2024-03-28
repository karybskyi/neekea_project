from django import forms


class CheckoutForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    delivery_required = forms.ChoiceField()
    shipping_address = forms.CharField(required=False)
    payment_by_card = forms.ChoiceField()

    # fist_name = forms.ChoiceField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Enter your name"
    #         }
    #     )
    # )
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Enter your last name",
    #         }
    #     )
    # )
    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Enter your phone number"
    #         }
    #     )
    # )
    # needs_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", False),
    #         ("1", True),
    #     ],
    #     initial=0,
    # )
    # shipping_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             "class": "form-control",
    #             "id": "shipping-address",
    #             "rows": 2,
    #             "placeholder": "Enter shipping address"                
    #         }
    #     ),
    #     required=False,
    # )
    # payment_by_card = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", "False"),
    #         ("1", "True"),
    #     ],
    #     initial="card"
    # )
    