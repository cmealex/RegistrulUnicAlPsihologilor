# Section 1 - get xls url 
import requests
from bs4 import BeautifulSoup
import pandas as pd

columns = ['Numele (nume anterior) și prenumele','Cod personal']

pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

def getExcel():
    URL = "https://www.copsi.ro/index.php/registre"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    el = soup.find("a", string="Descărcați fișierul...")
    link_url = el["href"]

    print("link_url:", link_url)
    # should print '/images/RUP_Partea_I_-_Atestate_de_liberă_practică-05.07.2023.xlsx'

    prefix = "https://www.copsi.ro/"
    fillUrl = prefix + link_url
    print("fillUrl:", fillUrl)
    #should print: https://www.copsi.ro/images/RUP_Partea_I_-_Atestate_de_liberă_practică-05.07.2023.xlsx

    # Section 2 - get excel by url and save html file 
    excelFile = requests.get(fillUrl)
    open('downloadedRUP.xlsx', 'wb').write(excelFile.content)

def parseExcel(fileName = 'downloadedRUP.xlsx'):

    df = pd.read_excel(fileName)
    return df

    
    #print('allHeaders:', allHeaders)

def getAllHeaders(df):
    allHeaders = list(df.columns)
    return allHeaders 

def getIndexByPartialColumnName(myArray, myPartialColumnName):
    # using in
    result = list(filter(lambda x: myPartialColumnName in x, myArray))
    myIndex = myArray.index(result[0])
    #print ("resultFilteredList and index:", result[0], myIndex)
    return myIndex

def getItemsByName(df, name = "Simion"):
    allHeaders = getAllHeaders(df)
    allItemsWithName = df.loc[df[columns[0]].str.contains(name), allHeaders]
    return allItemsWithName

def returnGeneratedHTML(df):
    
    html_script = '''
  <script>

  let input = document.getElementById("myInput");
  let button = document.getElementById("myButton");
  input.addEventListener("input", stateHandle);
  function stateHandle() {
      if (document.getElementById("myInput").value.length > 3) {
          button.disabled = false;
      } else {
          button.disabled = true; 
      }
  }

  input.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      document.getElementById("myButton").click();
    }
  });


function showTable() {
  document.getElementById("divTable").style.display = "";
  document.getElementById("myButton").style.display = "none";
  document.getElementById("myButton2").style.display = "";
  document.getElementById("myInfo").style.display = "";

  let input = document.getElementById("myInput");
  input.addEventListener("keydown", function(event) {
    if (event.keyCode == 8 || event.keyCode == 46) {
      event.preventDefault();
    }
  });

}

function refreshPage() {
  window.location.reload();
}

function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementsByClassName("myTable");
  tr = document.getElementsByTagName("tr"); //was table before

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[7]; //TODO make dynamic?
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
</script>

    '''

    myIndex = getIndexByPartialColumnName(getAllHeaders(df), "Nume")
    #print("myIndex", myIndex)
    #

    html_string = '''
    <html>
    <head><title>RUP</title></head>
    <link rel="stylesheet" type="text/css" href="other.css"/>
    <body>
        <div class="wrap-flex">
          <input class="input" type="text" id="myInput" onkeyup="myFunction()"  placeholder="Cautati folosind: Nume Prenume (minim 4 caractere)">
          <button class="submit" type="submit" id="myButton" onclick="showTable()" disabled="disabled">Afiseaza tabelul</button>
          <button class="submit" type="submit" id="myButton2" onclick="refreshPage()" style="display: none;">Cautare noua</button>
          <p id="myInfo" style="display: none;"> (Daca doriti sa cautati alt psiholog, dati click pe "Cautare noua" - <u> nu puteti sterge textul introdus </u>)
          </p>
          </br>
        </div>
        <div id="divTable" style="display: none;">
        {table}
        </div>
        {script}
    </body>
    </html>
    '''

    with open('templates/RUP.html', 'w', encoding="utf-8") as f:
        f.write(html_string.format(script=html_script, table=df.to_html(classes='myTable', index=False, justify="right", table_id="myTableID", ))) 

    #TODO still .. https://www.w3schools.com/howto/howto_js_filter_table.asp
    #or:
    #https://www.codewithfaraz.com/content/9/how-to-create-a-filtersearch-html-table-with-few-lines-of-jquery
    #or 
    #https://www.geeksforgeeks.org/how-to-perform-a-real-time-search-and-filter-on-a-html-table/

    #TODO using Flask https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates

#other examples:
#https://stackoverflow.com/questions/56627967/pythonic-way-to-apply-a-filter-to-a-table
#https://www.listendata.com/2019/07/how-to-filter-pandas-dataframe.html

#getExcel()

df = parseExcel()
#allNameItems = getItemsByName(df, "Simion")
#print("allNameItems:", allNameItems)
returnGeneratedHTML(df)
