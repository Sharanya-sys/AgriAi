**# AgriAi**
A Streamlit web app using TensorFlow to detect crop diseases from photos, provide treatment advice, and integrate weather alerts for farmers. Built with Python—scalable for agriculture.

__STEPS:__

1. __Install Python__
    from python.org
   (Python 3.11 preffered)

2.**Create project folder 'AgriAi_Project'**
    add -  app.py, model.py and requirements.txt files inside this folder.

3.**Make and active virtual environment**
    Open terminal/ command prompt inside the project folder.

    ``` bash
     
      python -m venv env
      env\Scripts\activate
         ```

4. **Install required libraries**
   Run this in terminal
   
   ```bash
   
    pip install tensorflow keras numpy opencv-python pillow streamlit spicy
    ```

   

6.**Download dataset for plant leaf images.**
   * Go to Kaggle- Plantvillage or any source
   * download it and unzip
   * Move the images into separate folder(plantpic_kaggle).

7.**Train the model**
    In terminal run:
   
    ```bash
    
       python module.py
       ```
       
   This will train the model and save models/plant_disease_model.h5.

7.**Run the web app**
 To open the app..
   
   ```bash

   streamlit run app.py
   ```

   A browser window will open. Upload a leaf image and see prediction.

**Weather API key setup:**

 1. Go to OpenWeatherMap.
 2. Sign up and copy your API key.
 3. Add this key to code in app.py.
