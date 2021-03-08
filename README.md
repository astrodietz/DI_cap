# DI_cap

http://astrodietz.pythonanywhere.com/

This repo contains all pertinent files for my TDI capstone project (link to site above).

Site purpose: allows users to find "dupes" for skincare products, based on ingredients lists.
Users can tweak price range, and specify specific ingredients to be included/excluded in results.

ulta_products_CLEAN.pkd: array of skincare product info scraped from ulta.com

flask_app.py: website setup
find_match.py: match function retrieves top ~3 best product suggestions, based on ingredient list similarity

main_page.html: html for homepage
results_page.html: html for displaying match results
error_page.html: html for 'something went wrong...'

base.css: css for homepage + error page
results.css: css for results page
