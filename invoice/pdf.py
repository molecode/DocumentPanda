import os

from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize

from django.conf import settings
from django.template import defaultfilters

PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]
FONT = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
FONT_SIZE = 11
LEFT_PADDING = 55


def create_pdf(invoice):
    file_name = f'Rechnung_{invoice.invoice_number}_{invoice.your_full_name}.pdf'
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    can = canvas.Canvas(file_path)

    can.setFont(FONT, FONT_SIZE)
    can.drawString(LEFT_PADDING, 780, invoice.your_full_name)
    can.drawString(LEFT_PADDING, 765, invoice.your_street)
    can.drawString(LEFT_PADDING, 750, invoice.your_city)

    can.drawString(LEFT_PADDING, 710, invoice.customer_name)
    can.drawString(LEFT_PADDING, 695, invoice.customer_street)
    can.drawString(LEFT_PADDING, 680, invoice.customer_city)

    can.drawString(LEFT_PADDING, 640, 'Rechnungnummer: ')
    if invoice.contract_number:
        can.drawString(LEFT_PADDING, 625, 'Kunde: ')
        can.drawString(LEFT_PADDING, 610, 'Beratervertrag: ')
    can.drawString(LEFT_PADDING + 400, 610, 'Datum: ')

    can.setFont(FONT_BOLD, FONT_SIZE)
    can.drawString(LEFT_PADDING + 110, 640, invoice.invoice_number)
    if invoice.contract_number:
        can.drawString(LEFT_PADDING + 110, 625, invoice.month_report.customer.name)
        can.drawString(LEFT_PADDING + 110, 610, invoice.contract_number)
    can.drawString(LEFT_PADDING + 440, 610, defaultfilters.date(invoice.invoice_date, 'd. M. Y'))

    can.setFont(FONT_BOLD, 28)
    text = 'Rechnung'
    text_width = stringWidth(text, FONT_BOLD, 28)
    can.drawString((PAGE_WIDTH - text_width) / 2.0, 530, text)

    can.setFont(FONT, FONT_SIZE)
    can.drawString(LEFT_PADDING, 470, 'Leistungszeitraum: ')
    can.setFont(FONT_BOLD, FONT_SIZE)
    can.drawString(LEFT_PADDING + 110, 470, f'{invoice.invoice_period_begin.strftime("%d.%m.%Y")} - {invoice.invoice_period_end.strftime("%d.%m.%Y")}')

    rate = 'Rate/Einheit'
    anzahl = 'Anzahl'
    betrag = 'Betrag (€)'
    rate_width = stringWidth(rate, FONT_BOLD, FONT_SIZE)
    anzahl_width = stringWidth(anzahl, FONT_BOLD, FONT_SIZE)
    betrag_width = stringWidth(betrag, FONT_BOLD, FONT_SIZE)
    can.drawString(LEFT_PADDING, 430, 'Aktivität')
    can.drawString(LEFT_PADDING + 250, 430, rate)
    can.drawString(LEFT_PADDING + 350, 430, anzahl)
    can.drawString(LEFT_PADDING + 450, 430, betrag)
    can.line(LEFT_PADDING, 428, LEFT_PADDING + 450 + betrag_width, 428)

    rate_value = str(invoice.month_report.fee)
    anzahl_value = str(invoice.month_report.hours)
    betrag_value = str(invoice.month_report.brutto)
    rate_value_width = stringWidth(rate_value, FONT, FONT_SIZE)
    anzahl_value_width = stringWidth(anzahl_value, FONT, FONT_SIZE)
    betrag_value_width = stringWidth(betrag_value, FONT, FONT_SIZE)
    can.setFont(FONT, FONT_SIZE)
    can.drawString(LEFT_PADDING, 415, invoice.activity)
    can.drawString(LEFT_PADDING + 250 + rate_width - rate_value_width, 415, rate_value)
    can.drawString(LEFT_PADDING + 350 + anzahl_width - anzahl_value_width, 415, anzahl_value)
    can.drawString(LEFT_PADDING + 450 + betrag_width - betrag_value_width, 415, betrag_value)

    mwst_value = str(invoice.month_report.vat)
    mwst_value_width = stringWidth(mwst_value, FONT, FONT_SIZE)
    can.drawString(LEFT_PADDING, 350, 'MWSt. (19%)')
    can.drawString(LEFT_PADDING + 450 + betrag_width - mwst_value_width, 350, mwst_value)
    can.line(LEFT_PADDING, 345, LEFT_PADDING + 450 + betrag_width, 345)

    can.setFont(FONT_BOLD, FONT_SIZE)
    total_value = str(invoice.month_report.brutto_vat)
    total_value_width = stringWidth(total_value, FONT, FONT_SIZE)
    can.drawString(LEFT_PADDING, 330, 'Gesamtsumme')
    can.drawString(LEFT_PADDING + 450 + betrag_width - total_value_width, 330, total_value)

    can.setFont(FONT, FONT_SIZE)
    can.drawString(LEFT_PADDING, 300, 'Das Dokument der Zeiterfassung ist beigefügt.')
    can.drawString(LEFT_PADDING, 250, 'Mit freundlichen Grüßen')
    can.drawString(LEFT_PADDING, 200, 'Timo Schäpe')

    email = 'Email: '
    email_value = f'{invoice.email}  -  '
    ust = 'USt-IdNr.: '
    ust_value = invoice.turnover_tax_number
    email_width = stringWidth(email, FONT, FONT_SIZE)
    email_value_width = stringWidth(email_value, FONT_BOLD, FONT_SIZE)
    ust_width = stringWidth(ust, FONT, FONT_SIZE)
    ust_value_width = stringWidth(ust_value, FONT_BOLD, FONT_SIZE)

    email_start = (PAGE_WIDTH - (email_width + email_value_width + ust_width + ust_value_width)) / 2.0
    email_value_start = email_start + email_width + 1
    ust_start = email_value_start + email_value_width
    ust_value_start = ust_start + ust_width + 1

    bank = 'Bankverbindung: '
    bank_value = f'{invoice.bank_name}  -  '
    iban = 'IBAN: '
    iban_value = f'{invoice.iban}  -  '
    bic = 'BIC: '
    bic_value = invoice.bic

    bank_width = stringWidth(bank, FONT, FONT_SIZE)
    bank_value_width = stringWidth(bank_value, FONT_BOLD, FONT_SIZE)
    iban_width = stringWidth(iban, FONT, FONT_SIZE)
    iban_value_width = stringWidth(iban_value, FONT_BOLD, FONT_SIZE)
    bic_width = stringWidth(bic, FONT, FONT_SIZE)
    bic_value_width = stringWidth(bic_value, FONT_BOLD, FONT_SIZE)

    bank_start = (PAGE_WIDTH - (bank_width + bank_value_width + iban_width + iban_value_width + bic_width + bic_value_width)) / 2.0
    bank_value_start = bank_start + bank_width + 1
    iban_start = bank_value_start + bank_value_width
    iban_value_start = iban_start + iban_width + 1
    bic_start = iban_value_start + iban_value_width
    bic_value_start = bic_start + bic_width + 1

    can.drawString(email_start, 90, email)
    can.drawString(ust_start, 90, ust)

    can.drawString(bank_start, 75, bank)
    can.drawString(iban_start, 75, iban)
    can.drawString(bic_start, 75, bic)

    can.setFont(FONT_BOLD, FONT_SIZE)
    can.drawString(email_value_start, 90, email_value)
    can.drawString(ust_value_start, 90, ust_value)

    can.drawString(bank_value_start, 75, bank_value)
    can.drawString(iban_value_start, 75, iban_value)
    can.drawString(bic_value_start, 75, bic_value)

    can.showPage()
    can.save()

    invoice.file_path = file_path
    invoice.save()
