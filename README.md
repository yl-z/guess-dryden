# guess-dryden
trying to visualize how far machine translation can currently take us towards high-brow literary translation

Currently, this project contains twelve books of the Aeneid (in both Latin and Dryden's highly literary English) scraped from the web and passed through the Google Translate API. 
Edit distance is used to match translation results with the target language text. The resulting graphs (data in json files) show where a lot of literary license was taken and which lines in a relevant neighbourhood can be guessed to have "come from" which original line.
I am still working on the javascript for displaying this dynamically on a webpage. 
