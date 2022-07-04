![image](https://user-images.githubusercontent.com/51901867/177068986-663dca95-4df5-4117-91a7-41dc19f7ed6c.png)
Credits of picture taken from here:https://dailyhive.com/vancouver/vancouver-housing-market-correction

<h1>Description</h1>

Canada is very known for its hot housing market. Howwever, that sort of data is not readily avaiable to by avid housing readers. Even if it is available, the data may not be fully complete. Luckily, with the use of technology, web scraping made it possible to retrieve this data. The script in thie repository will collect sold housing data (and features) within the Greater Vancouver Area (Canada)


<h1>Preview</h1>

Preview of the webpage is shown below

![image](https://user-images.githubusercontent.com/51901867/177067568-3a4157d7-6f27-4982-8089-d556e31b55a0.png)

The dataset will consist the following variables:
- MLS Number
- Street Address
- Postal Code
- Neighborhood
- City
- Property Type
- Property Style
- Property Age
- Sold Price
- Ask Price
- Original Price
- Mainitenance Price
- Bedrooms
- Bathrooms
- Size (in sqft)
- Reported Sold Date
- Sld Date
- On Market (in days)
- Listing Brokerage
- Buying Brokerage
- Price per sqft
- Maintenance per sqft

<h1> How to run this project </h1>
1. Download zip or clone it using 'git clone https://github.com/alancflau/housing_prices.git'
2. Unzip the downloaded file
3. Run command 'pip install -r requirements.txt' to install the dependencies
4. Run the project by using python main.py from the directory you have stored the file


<h1> Next Steps </h1>
1. The current script can be run with a push of the button. Next step is to automate such that it runs on a daily basis. This can be done on a server or locally (Task scheduler)<br>
2. Collect more data and perform analysis which areas are hotspots to purchase a house. Determine the price ranges for each neighborhood/city <br>
3. Once there is enough data, create a machine learning model to predict the price a house would be sold given a set of attributes
