review = bbs.find("span", {"class":"IirT-rating-category"})
    reviewcount = bbs.find("span", {"class":"IirT-rating-count"}).text 
    rating = bbs.find("span", {"class": "eddo-rating-score"}).text
    BookingsPrice = bbs.find("span",{"class":"D8J--price"}).text