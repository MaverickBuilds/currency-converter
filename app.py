from flask import Flask, render_template, request
from datetime import datetime, timedelta
import requests
import os

app = Flask(__name__)

  # Cache variables

currency_info = {
    "USD": {"name": "United States Dollar", "symbol": "$"},
    "AED": {"name": "United Arab Emirates Dirham", "symbol": "د.إ"},
    "AFN": {"name": "Afghan Afghani", "symbol": "؋"},
    "ALL": {"name": "Albanian Lek", "symbol": "L"},
    "AMD": {"name": "Armenian Dram", "symbol": "֏"},
    "ANG": {"name": "Netherlands Antillean Guilder", "symbol": "ƒ"},
    "AOA": {"name": "Angolan Kwanza", "symbol": "Kz"},
    "ARS": {"name": "Argentine Peso", "symbol": "$"},
    "AUD": {"name": "Australian Dollar", "symbol": "$"},
    "AWG": {"name": "Aruban Florin", "symbol": "ƒ"},
    "AZN": {"name": "Azerbaijani Manat", "symbol": "₼"},
    "BAM": {"name": "Bosnia-Herzegovina Convertible Mark", "symbol": "KM"},
    "BBD": {"name": "Barbadian Dollar", "symbol": "$"},
    "BDT": {"name": "Bangladeshi Taka", "symbol": "৳"},
    "BGN": {"name": "Bulgarian Lev", "symbol": "лв"},
    "BHD": {"name": "Bahraini Dinar", "symbol": ".د.ب"},
    "BIF": {"name": "Burundian Franc", "symbol": "Fr"},
    "BMD": {"name": "Bermudian Dollar", "symbol": "$"},
    "BND": {"name": "Brunei Dollar", "symbol": "$"},
    "BOB": {"name": "Bolivian Boliviano", "symbol": "Bs."},
    "BRL": {"name": "Brazilian Real", "symbol": "R$"},
    "BSD": {"name": "Bahamian Dollar", "symbol": "$"},
    "BTN": {"name": "Bhutanese Ngultrum", "symbol": "Nu."},
    "BWP": {"name": "Botswanan Pula", "symbol": "P"},
    "BYN": {"name": "Belarusian Ruble", "symbol": "Br"},
    "BZD": {"name": "Belize Dollar", "symbol": "$"},
    "CAD": {"name": "Canadian Dollar", "symbol": "$"},
    "CDF": {"name": "Congolese Franc", "symbol": "Fr"},
    "CHF": {"name": "Swiss Franc", "symbol": "Fr"},
    "CLF": {"name": "Chilean Unit of Account (UF)", "symbol": "UF"},
    "CLP": {"name": "Chilean Peso", "symbol": "$"},
    "CNH": {"name": "Chinese Yuan (Offshore)", "symbol": "¥"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥"},
    "COP": {"name": "Colombian Peso", "symbol": "$"},
    "CRC": {"name": "Costa Rican Colón", "symbol": "₡"},
    "CUP": {"name": "Cuban Peso", "symbol": "$"},
    "CVE": {"name": "Cape Verdean Escudo", "symbol": "$"},
    "CZK": {"name": "Czech Koruna", "symbol": "Kč"},
    "DJF": {"name": "Djiboutian Franc", "symbol": "Fr"},
    "DKK": {"name": "Danish Krone", "symbol": "kr"},
    "DOP": {"name": "Dominican Peso", "symbol": "$"},
    "DZD": {"name": "Algerian Dinar", "symbol": "د.ج"},
    "EGP": {"name": "Egyptian Pound", "symbol": "£"},
    "ERN": {"name": "Eritrean Nakfa", "symbol": "Nfk"},
    "ETB": {"name": "Ethiopian Birr", "symbol": "Br"},
    "EUR": {"name": "Euro", "symbol": "€"},
    "FJD": {"name": "Fijian Dollar", "symbol": "$"},
    "FKP": {"name": "Falkland Islands Pound", "symbol": "£"},
    "FOK": {"name": "Faroese Króna", "symbol": "kr"},
    "GBP": {"name": "British Pound Sterling", "symbol": "£"},
    "GEL": {"name": "Georgian Lari", "symbol": "₾"},
    "GGP": {"name": "Guernsey Pound", "symbol": "£"},
    "GHS": {"name": "Ghanaian Cedi", "symbol": "₵"},
    "GIP": {"name": "Gibraltar Pound", "symbol": "£"},
    "GMD": {"name": "Gambian Dalasi", "symbol": "D"},
    "GNF": {"name": "Guinean Franc", "symbol": "Fr"},
    "GTQ": {"name": "Guatemalan Quetzal", "symbol": "Q"},
    "GYD": {"name": "Guyanaese Dollar", "symbol": "$"},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "$"},
    "HNL": {"name": "Honduran Lempira", "symbol": "L"},
    "HRK": {"name": "Croatian Kuna", "symbol": "kn"},
    "HTG": {"name": "Haitian Gourde", "symbol": "G"},
    "HUF": {"name": "Hungarian Forint", "symbol": "Ft"},
    "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp"},
    "ILS": {"name": "Israeli New Shekel", "symbol": "₪"},
    "IMP": {"name": "Isle of Man Pound", "symbol": "£"},
    "INR": {"name": "Indian Rupee", "symbol": "₹"},
    "IQD": {"name": "Iraqi Dinar", "symbol": "ع.د"},
    "IRR": {"name": "Iranian Rial", "symbol": "﷼"},
    "ISK": {"name": "Icelandic Króna", "symbol": "kr"},
    "JEP": {"name": "Jersey Pound", "symbol": "£"},
    "JMD": {"name": "Jamaican Dollar", "symbol": "$"},
    "JOD": {"name": "Jordanian Dinar", "symbol": "د.ا"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥"},
    "KES": {"name": "Kenyan Shilling", "symbol": "Sh"},
    "KGS": {"name": "Kyrgystani Som", "symbol": "с"},
    "KHR": {"name": "Cambodian Riel", "symbol": "៛"},
    "KID": {"name": "Kiribati Dollar", "symbol": "$"},
    "KMF": {"name": "Comorian Franc", "symbol": "Fr"},
    "KRW": {"name": "South Korean Won", "symbol": "₩"},
    "KWD": {"name": "Kuwaiti Dinar", "symbol": "د.ك"},
    "KYD": {"name": "Cayman Islands Dollar", "symbol": "$"},
    "KZT": {"name": "Kazakhstani Tenge", "symbol": "₸"},
    "LAK": {"name": "Laotian Kip", "symbol": "₭"},
    "LBP": {"name": "Lebanese Pound", "symbol": "ل.ل"},
    "LKR": {"name": "Sri Lankan Rupee", "symbol": "Rs"},
    "LRD": {"name": "Liberian Dollar", "symbol": "$"},
    "LSL": {"name": "Lesotho Loti", "symbol": "L"},
    "LYD": {"name": "Libyan Dinar", "symbol": "ل.د"},
    "MAD": {"name": "Moroccan Dirham", "symbol": "د.م."},
    "MDL": {"name": "Moldovan Leu", "symbol": "L"},
    "MGA": {"name": "Malagasy Ariary", "symbol": "Ar"},
    "MKD": {"name": "Macedonian Denar", "symbol": "ден"},
    "MMK": {"name": "Myanmar Kyat", "symbol": "K"},
    "MNT": {"name": "Mongolian Tugrik", "symbol": "₮"},
    "MOP": {"name": "Macanese Pataca", "symbol": "P"},
    "MRU": {"name": "Mauritanian Ouguiya", "symbol": "UM"},
    "MUR": {"name": "Mauritian Rupee", "symbol": "₨"},
    "MVR": {"name": "Maldivian Rufiyaa", "symbol": "Rf"},
    "MWK": {"name": "Malawian Kwacha", "symbol": "MK"},
    "MXN": {"name": "Mexican Peso", "symbol": "$"},
    "MYR": {"name": "Malaysian Ringgit", "symbol": "RM"},
    "MZN": {"name": "Mozambican Metical", "symbol": "MT"},
    "NAD": {"name": "Namibian Dollar", "symbol": "$"},
    "NGN": {"name": "Nigerian Naira", "symbol": "₦"},
    "NIO": {"name": "Nicaraguan Córdoba", "symbol": "C$"},
    "NOK": {"name": "Norwegian Krone", "symbol": "kr"},
    "NPR": {"name": "Nepalese Rupee", "symbol": "₨"},
    "NZD": {"name": "New Zealand Dollar", "symbol": "$"},
    "OMR": {"name": "Omani Rial", "symbol": "ر.ع."},
    "PAB": {"name": "Panamanian Balboa", "symbol": "B/."},
    "PEN": {"name": "Peruvian Nuevo Sol", "symbol": "S/."},
    "PGK": {"name": "Papua New Guinean Kina", "symbol": "K"},
    "PHP": {"name": "Philippine Peso", "symbol": "₱"},
    "PKR": {"name": "Pakistani Rupee", "symbol": "₨"},
    "PLN": {"name": "Polish Zloty", "symbol": "zł"},
    "PYG": {"name": "Paraguayan Guarani", "symbol": "₲"},
    "QAR": {"name": "Qatari Rial", "symbol": "ر.ق"},
    "RON": {"name": "Romanian Leu", "symbol": "lei"},
    "RSD": {"name": "Serbian Dinar", "symbol": "дин"},
    "RUB": {"name": "Russian Ruble", "symbol": "₽"},
    "RWF": {"name": "Rwandan Franc", "symbol": "Fr"},
    "SAR": {"name": "Saudi Riyal", "symbol": "ر.س"},
    "SBD": {"name": "Solomon Islands Dollar", "symbol": "$"},
    "SCR": {"name": "Seychellois Rupee", "symbol": "₨"},
    "SDG": {"name": "Sudanese Pound", "symbol": "ج.س."},
    "SEK": {"name": "Swedish Krona", "symbol": "kr"},
    "SGD": {"name": "Singapore Dollar", "symbol": "$"},
    "SHP": {"name": "Saint Helena Pound", "symbol": "£"},
    "SLE": {"name": "Sierra Leonean Leone", "symbol": "Le"},
    "SLL": {"name": "Sierra Leonean Leone (Old)", "symbol": "Le"},
    "SOS": {"name": "Somali Shilling", "symbol": "Sh"},
    "SRD": {"name": "Surinamese Dollar", "symbol": "$"},
    "SSP": {"name": "South Sudanese Pound", "symbol": "£"},
    "STN": {"name": "São Tomé and Príncipe Dobra", "symbol": "Db"},
    "SYP": {"name": "Syrian Pound", "symbol": "£"},
    "SZL": {"name": "Swazi Lilangeni", "symbol": "L"},
    "THB": {"name": "Thai Baht", "symbol": "฿"},
    "TJS": {"name": "Tajikistani Somoni", "symbol": "ЅМ"},
    "TMT": {"name": "Turkmenistani Manat", "symbol": "m"},
    "TND": {"name": "Tunisian Dinar", "symbol": "د.ت"},
    "TOP": {"name": "Tongan Paʻanga", "symbol": "T$"},
    "TRY": {"name": "Turkish Lira", "symbol": "₺"},
    "TTD": {"name": "Trinidad and Tobago Dollar", "symbol": "$"},
    "TVD": {"name": "Tuvaluan Dollar", "symbol": "$"},
    "TWD": {"name": "New Taiwan Dollar", "symbol": "$"},
    "TZS": {"name": "Tanzanian Shilling", "symbol": "Sh"},
    "UAH": {"name": "Ukrainian Hryvnia", "symbol": "₴"},
    "UGX": {"name": "Ugandan Shilling", "symbol": "Sh"},
    "UYU": {"name": "Uruguayan Peso", "symbol": "$"},
    "UZS": {"name": "Uzbekistan Som", "symbol": "so'm"},
    "VES": {"name": "Venezuelan Bolívar", "symbol": "Bs."},
    "VND": {"name": "Vietnamese Dong", "symbol": "₫"},
    "VUV": {"name": "Vanuatu Vatu", "symbol": "Vt"},
    "WST": {"name": "Samoan Tala", "symbol": "T"},
    "XAF": {"name": "Central African CFA Franc", "symbol": "Fr"},
    "XCD": {"name": "East Caribbean Dollar", "symbol": "$"},
    "XCG": {"name": "Caribbean Guilder", "symbol": "ƒ"},
    "XDR": {"name": "Special Drawing Rights", "symbol": "SDR"},
    "XOF": {"name": "West African CFA Franc", "symbol": "Fr"},
    "XPF": {"name": "CFP Franc", "symbol": "Fr"},
    "YER": {"name": "Yemeni Rial", "symbol": "﷼"},
    "ZAR": {"name": "South African Rand", "symbol": "R"},
    "ZMW": {"name": "Zambian Kwacha", "symbol": "ZK"},
    "ZWG": {"name": "Zimbabwean Gold", "symbol": "$"},
    "ZWL": {"name": "Zimbabwean Dollar", "symbol": "$"}
}


last_fetch_time = None
cached_rates = None
api_error = None

def get_rates():
    global last_fetch_time, cached_rates, api_error
    api_error = None
    if last_fetch_time is None:
        try:
            response = os.getenv("API_KEY")
            data = response.json()
            cached_rates = data
            last_fetch_time = datetime.now()
        except:
            api_error = "An error has occured, please try again later"
            print (api_error)

    else:
        time_passed = datetime.now() - last_fetch_time
        if time_passed > timedelta(hours=24):
            try:
                response = requests.get("https://v6.exchangerate-api.com/v6/96969edce2ff6bf8ba9f3088/latest/USD")
                data = response.json()
                cached_rates = data
                last_fetch_time = datetime.now()
            except:
                pass


@app.route('/', methods=['GET'])

def home():
    result = None
    amount = None
    from_currency = "USD"
    to_currency = "USD"
    get_rates()

    if last_fetch_time:
        formatted_time = last_fetch_time.strftime("%H:%M %d/%m/%Y")
    else:
        formatted_time = None

    return render_template('index.html', result=result, amount=amount, formatted_time=formatted_time, cached_rates=cached_rates, from_currency=from_currency, to_currency=to_currency, api_error=api_error, currency_info=currency_info)

if __name__ == '__main__':
    app.run(debug=True)