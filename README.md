# Wallpaper Catalog Ingest

This project is created with the sole purpose of extracting data from an e-commerce website.

This extracted data then gets saved into a .csv file.

Website link: [Click Here](https://www.yorkwallcoverings.com/wallpaper-york)

### Target Data:

This data is what we are extracting from the website including:

  1. SKU

  2. Product Name

  3. Brand 

  4. Collection

  5. Sizes

  6. Availability

  7. Price

  8. Material

  9. Installation

  10. Repeat

  11. Match

  12. Roll Width

  13. Roll Coverage

  14. Washability

  15. Removability

  16. Roll Length

  17. Image link

<br>

The screenshots given below are taken from the target website:

<br>

<img src="assets/target_data1.png" width="60%">

<img src="assets/target_data2.png" width="70%">

### Demo


<video src="assets/terminal_recording_new.mp4" controls></video>


You can check the sample of spreadsheet created during the recording of this video right here:

[Preview File](https://www.dropbox.com/scl/fi/3raqxla11ze8ajrb3j2dm/Wallpaper_listings.csv?rlkey=0o4q61togtrfjdew8nxwre0p7&st=b1c1h2az&dl=0) | [Download](https://www.dropbox.com/scl/fi/3raqxla11ze8ajrb3j2dm/Wallpaper_listings.csv?rlkey=0o4q61togtrfjdew8nxwre0p7&st=b1c1h2az&dl=1) 

### How does it work?

This project is a 2 stage data extraction pipeline which:

1. It grabs the product links from - all wallpapers page

2. Then it visits the product page one by one, extracting data in the process.

### Benefits of creating a pipeline

If you don't want to waste hours manually typing thousands of product details into a spreadsheet, this tool is the perfect solution.

If you wanted the updated data from the website, this project can do this in one click! However, it will take some time.

This is a data pipeline which is connected to the e-commerce site, which means this script isn't just limited for creating .csv file. You can change the direction of the pipe to create whatever kind of file u want - database file, Excel file, Word file, PDF's etc. The only catch is: It has to be a file which can take the data and handle it!
