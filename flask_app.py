from flask import Flask, request, render_template
from find_match import match #product-matching function

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def main_page():

    if request.method == "POST": #user has made a query

        product = None
        try:
            product = str(request.form["product"]) #grab query
        except Exception:
            return render_template("error_page.html") #invalid query type

        try:
            max_price=float(request.form["max_price"].strip('$')) #grab (optional) param
        except Exception:
            max_price=None

        try:
            include=str(request.form["include"]).split(", ") #grab (optional) param
            include=[ingr.lower() for ingr in include]
            if(include==[""]):
                include=None
        except Exception:
            include=None

        try:
            exclude=str(request.form["exclude"]).split(", ") #grab (optional) param
            exclude=[ingr.lower() for ingr in exclude]
            if(exclude==[""]):
                exclude=None
        except Exception:
            exclude=None

        if len(product)>0:

            found, result = match(product,max_price,include,exclude) #try to match
            if(found==False): #no match!
                return render_template("main_page.html",vars=result)
            else: #display match info
                return render_template("results_page.html",vars=result)

        else: #empty search
            return render_template("error_page.html")

    return render_template("main_page.html",vars='')
