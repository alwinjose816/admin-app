import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
from supabase import create_client
st.set_page_config(layout="wide")
# ---------------- SUPABASE ----------------
url = "https://yewmxtzbygmcaicpmxfz.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlld214dHpieWdtY2FpY3BteGZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5NzM5MzgsImV4cCI6MjA5MDU0OTkzOH0.3KzP09-g4ThJg9JuZZ2jbVrCLhCtIDuWkc13lvqAgzg"
supabase = create_client(url, key)

# ---------------- PAGE ----------------
st.set_page_config(page_title="Admin Login", layout="wide")
st.markdown("""
  <style>
  /* warning box */
  div[data-testid="stAlert"] {
    background-color: #fff8cc !important;
    border-radius: 10px !important;
}

  /* warning text inside box */
  div[data-testid="stAlert"] p {
    color: #000000 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}
  </style>
""", unsafe_allow_html=True)
# ---------------- STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- STYLE ----------------

st.markdown("""
  <style>
 /* full app font */
 .stApp {
    background-color: #ffffff;
    font-family: 'Poppins', sans-serif;
}

/* label text */
label {
    color: #ED1C24 !important;
    font-weight: 900;
    font-style: italic;
}

/* heading text */
h2 {
    color: #ED1C24 !important;
    font-family: 'Poppins', sans-serif;
    font-weight: 100;
}

/* remove background of input container */
div[data-testid="stTextInput"] {
    background: transparent !important;
}

/* actual input field */
div[data-testid="stTextInput"] input {
    background-color: transparent !important;
    color: #2744A0 !important;

    border: none !important;
    border-bottom: 2px solid #2744A0 !important;

    border-radius: 0px !important;
    padding: 8px 0px !important;
    height: 40px !important;
    font-size: 16px !important;

    box-shadow: none !important;
}

/* focus effect */
div[data-testid="stTextInput"] input:focus {
    outline: none !important;
    border-bottom: 3px solid #ED1C24 !important;
}


/* make input width smaller */
div[data-testid="stTextInput"] {
    width: 50% !important;
}

/* button text */
.stButton button {
    color: #ffffff !important;
    background-color: #0067B8 !important;
    font-family: 'Poppins', sans-serif;
    font-weight: bold;
    min-width: 180px;
    height: 50px;
    width: auto;
    border-radius: 8px;
}

.block-container {
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 2rem;
    max-width: 80% !important;
}


/* card */
.main-card {
    background-color: #2744A0;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    font-family: 'Poppins', sans-serif;
}
/* Fix date picker overlapping issue */
div[data-baseweb="popover"] {
    z-index: 9999 !important;
}

/* Optional: make sure dropdowns also stay on top */
div[role="listbox"] {
    z-index: 9999 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.markdown(
    "<h2 style='color: #1e7df0;'>Admin Login</h2>",
    unsafe_allow_html=True
)

    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")

    col1, gap, col2 = st.columns([1, 0.2, 3])

    with col1:
        if st.button("LOGIN", use_container_width=True):
            try:
                supabase.auth.sign_in_with_password({
                    "email": email.strip(),
                    "password": password
                })
                st.success("Login successful")

            # ADD THESE LINES
                st.session_state.user_email = email.strip()
                st.session_state.page = "dashboard"
                st.rerun()

            except Exception as e:
                st.error(str(e))

    with col2:
        if st.button("NEW REGISTER", use_container_width=True):
            st.warning("Please contact admin to create your account.")

# ---------------- REGISTER PAGE ----------------
elif st.session_state.page == "dashboard":
    st.markdown("""
    <div style='text-align:center; margin-top:-10px; margin-bottom:20px;'>
        <h1 style='color:#2E86C1;'>🏢 Admin Application</h1>
    </div>
    """, unsafe_allow_html=True)

   
    import requests

    # default selected menu
    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = "DEPO"

    selected = st.session_state.selected_menu

    # ---------------- TOP MENU BUTTONS ----------------
    depo_color = "#ED1C24" if selected == "DEPO" else "#0067B8"
    dealer_color = "#ED1C24" if selected == "DEALER" else "#0067B8"
    monitor_color = "#ED1C24" if selected == "MONITOR" else "#0067B8"
    dashboard_color = "#ED1C24" if selected == "DASHBOARD" else "#0067B8"

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,0.8])

    with col1:
      label = "🔴 DEPO" if selected == "DEPO" else "DEPO"
      if st.button(label, key="depo_btn", use_container_width=True):
        st.session_state.selected_menu = "DEPO"
        st.rerun()

    with col2:
      label = "🔴 DEALER" if selected == "DEALER" else "DEALER"
      if st.button(label, key="dealer_btn", use_container_width=True):
        st.session_state.selected_menu = "DEALER"
        st.rerun()

    with col3:
      label = "🔴 MONITOR" if selected == "MONITOR" else "MONITOR"
      if st.button(label, key="monitor_btn", use_container_width=True):
        st.session_state.selected_menu = "MONITOR"   # ✅ FIXED
        st.rerun()
   
    with col4:
      label = "🔴 DASHBOARD" if selected == "DASHBOARD" else "DASHBOARD"
      if st.button(label, key="dashboard_btn", use_container_width=True):
        st.session_state.selected_menu = "DASHBOARD"
        st.rerun()
    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            try:
                 supabase.auth.sign_out()
            except:
                pass

            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    st.markdown("""
    <style>
    button[kind="secondary"] {
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ---------------- DEPO PAGE ----------------
    if selected == "DEPO":

    # ---------- TAB STYLE ----------
      st.markdown("""
       <style>
        button[data-baseweb="tab"] {
        color: #666666 !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        font-size: 16px !important;
    }

        button[data-baseweb="tab"][aria-selected="true"] {
        color: #ED1C24 !important;
        border-bottom: 3px solid #ED1C24 !important;
    }
         </style>
         """, unsafe_allow_html=True)

      tab1, tab2, tab3 = st.tabs(
        ["Depot Entry", "Stock Entry", "Stock List"]
      )

    # ================= DEPOT ENTRY =================
      with tab1:

          st.markdown(
            "<h1 style='color:#ED1C24; font-weight:800;'>Depot Entry</h1>",
            unsafe_allow_html=True
         )

          depot_name = st.text_input("Depot Name", key="depot_name")
          depot_code = st.text_input("Depot Code", key="depot_code")
          area_sqft = st.number_input(
            "Area (sq ft)",
            min_value=0.0,
            key="depot_area"
         )
         
          address = st.text_area("Full Address", key="depot_address")
         
          

          capacity_mt = area_sqft / 5
          st.write(f"Calculated Capacity: {capacity_mt:.2f} MT")
  
        # ---------- GET COORDINATES ----------
          if st.button("GET COORDINATES", key="get_coord_btn"):
             

             api_key = "AIzaSyD6kKoeqpSS76MSIg9kREgPsw2j_v1LmDo"

             url = "https://maps.googleapis.com/maps/api/geocode/json"

             params = {
                 "address": address.strip(),
                 "key": api_key
             }
             with st.spinner("Fetching location details..."):
                 response = requests.get(url, params=params, timeout=10)
                 data = response.json()
                 pin_data = response.json()
                 

             if data["status"] == "OK":
                 result = data["results"][0]
                 location = result["geometry"]["location"]

    # save coordinates
                 st.session_state["latitude"] = str(location["lat"])
                 st.session_state["longitude"] = str(location["lng"])
                 

                 temp_place = ""
                 temp_city = ""  
                 temp_district = ""
                 temp_state = ""

                 for comp in result["address_components"]:
                    types = comp["types"]

    # pincode
                    if "postal_code" in types:
                        st.session_state["depot_pincode"] = comp["long_name"]

    # place (small local area)
                    if any(t in types for t in [
                         "sublocality",
                         "sublocality_level_1",
                         "neighborhood"
                    ]):
                        if temp_place == "":
                           temp_place = comp["long_name"]

    # city
                    if "locality" in types:
                            temp_city = comp["long_name"]

    # district
                    if any(t in types for t in [
                        "administrative_area_level_2",
                        "administrative_area_level_3"
                    ]):
                        temp_district = comp["long_name"]

    # state
                    if "administrative_area_level_1" in types:
                       temp_state = comp["long_name"]
                          
               
                 
                 
                 # fetch place from pincode
                 # fetch place from pincode
                 if temp_place == "":
                    temp_place = temp_district

                 if temp_city == "":
                    temp_city = temp_district
                 if st.session_state.get("depot_pincode", "") == "":
                    rev_params = {
                      "latlng": f"{location['lat']},{location['lng']}",
                      "key": api_key
                    }

                    rev_response = requests.get(url, params=rev_params, timeout=10)
                    rev_data = rev_response.json()

                    if rev_data["status"] == "OK":
                      for comp in rev_data["results"][0]["address_components"]:
                        if "postal_code" in comp["types"]:
                           st.session_state["depot_pincode"] = comp["long_name"]
                           break
                 # district fallback
                 if temp_district == "":
                    temp_district = temp_city

# place fallback
                 if temp_place == "":
                    temp_place = temp_city
# fallback district
                
                # from Google first
                 

                 st.session_state["depot_place"] = temp_place
                 st.session_state["depot_city"] = temp_city
                 st.session_state["depot_district"] = temp_district
                 st.session_state["depot_state"] = temp_state

                 st.success("Coordinates and location details fetched successfully")
                 
                 st.markdown("<h3 style='color:black;'>Fetched Location Details</h3>", unsafe_allow_html=True)

                 st.markdown(f"<p style='color:black;'><b>Place:</b> {st.session_state.get('depot_place', '')}</p>", unsafe_allow_html=True)
                 st.markdown(f"<p style='color:black;'><b>City:</b> {st.session_state.get('depot_city', '')}</p>", unsafe_allow_html=True)
                 st.markdown(f"<p style='color:black;'><b>District:</b> {st.session_state.get('depot_district', '')}</p>", unsafe_allow_html=True                 )
                 st.markdown(f"<p style='color:black;'><b>Pincode:</b> {st.session_state.get('depot_pincode', '')}</p>", unsafe_allow_html=True)
                 st.markdown(f"<p style='color:black;'><b>State:</b> {st.session_state.get('depot_state', '')}</p>", unsafe_allow_html=True)
                 st.markdown(f"<p style='color:black;'><b>Latitude:</b> {st.session_state.get('latitude', '')}</p>", unsafe_allow_html=True)
                 st.markdown(f"<p style='color:black;'><b>Longitude:</b> {st.session_state.get('longitude', '')}</p>", unsafe_allow_html=True)
             else:
                st.error(f"Location not found: {data['status']}")
      

        # ---------- SAVE DEPOT ----------
          if st.button("SAVE DEPOT", use_container_width=True, key="save_depot_btn"):

                 if (
                     depot_name.strip() == "" or
                     depot_code.strip() == "" or
                     area_sqft <= 0 or
                     address.strip() == "" or
                     st.session_state.get("depot_pincode", "").strip() == "" or
                     
                     st.session_state.get("depot_district", "").strip() == "" or
                     st.session_state.get("depot_state", "").strip() == "" or

                     st.session_state.get("latitude", "").strip() == "" or
                     st.session_state.get("longitude", "").strip() == ""
                 ):
                    st.error("Please fill all fields before saving.")
                 else:

            
                   existing = supabase.table("depot_master") \
                    .select("depot_code") \
                    .eq("depot_code", depot_code) \
                    .execute()

                   if existing.data:
                      st.error("Depot Code already exists.")
                   else:
           
                       save_data = {
                        "depot_name": depot_name,
                        "depot_code": depot_code,
                        "place": st.session_state.get("depot_place", ""),
                        "city": st.session_state.get("depot_city", ""),
                        "district": st.session_state.get("depot_district", ""),
                        "state": st.session_state.get("depot_state", ""),
                        "pincode": st.session_state.get("depot_pincode", ""),
                        "address": address,
                        "area_sqft": area_sqft,
                        "capacity_mt": capacity_mt,
                        "latitude": st.session_state.get("latitude", ""),
                        "longitude": st.session_state.get("longitude", "")
                       }

                       supabase.table("depot_master") \
                        .insert(save_data) \
                        .execute()

                       st.success("Depot saved successfully")

     # ================= STOCK ENTRY =================
      with tab2:
         if "grn_products" not in st.session_state:
             st.session_state.grn_products = []

         st.markdown("## Stock Entry")

         sap_grn_number = st.text_input(
             "SAP GRN / Material Document No",
              key="sap_grn_number"
         )

         truck_number = st.text_input(
           "Truck Number",
           key="truck_number"
         )

         depot_data = supabase.table("depot_master") \
             .select("depot_code") \
             .execute()

         depot_codes = [row["depot_code"] for row in depot_data.data]

         stock_depot_code = st.selectbox(
             "Depot Code",
             options=depot_codes,
             index=None,
             placeholder="Type to search depot code",
             key="stock_entry_depot"
         )

         product_master_data = supabase.table("product_master") \
             .select("product_code, product_name") \
             .execute()

         product_names = [
             row["product_name"]
             for row in product_master_data.data
         ]

         selected_product_name = st.selectbox(
             "Product Name",
             options=product_names,
             index=None,
             placeholder="Type product name for suggestions",
             key="product_name_select"
         )

         product_code = ""

         if selected_product_name:
            matched_row = next(
              (
                row for row in product_master_data.data
                if row["product_name"].strip().lower()
                == selected_product_name.strip().lower()
              ),
              None
            )

            if matched_row is not None:
               product_code = matched_row["product_code"]

         st.info(f"Product Code: {product_code}")

         bag_weight = st.number_input(
             "Bag Weight (kg)",
             min_value=1.0,
             value=50.0,
             step=1.0,
             key="bag_weight"
         )

         number_of_bags = st.number_input(
              "Number of Bags",
              min_value=0,
              step=1,
              key="number_of_bags"
         )   

         stock_received = (number_of_bags * bag_weight) / 1000
         st.info(f"Stock Received (MT): {stock_received:.2f}")

         stock_received_date = st.date_input(
              "Stock Received Date",
               key="stock_received_date"
         )

         if st.button("ADD PRODUCT", key="add_product_btn"):
             current_code = str(product_code).strip().upper()

             existing_codes = {
               str(item["product_code"]).strip().upper()
               for item in st.session_state.grn_products
             }

             existing_db_item = supabase.table("depot_stock") \
                .select("id") \
                .eq("sap_grn_number", sap_grn_number) \
                .eq("product_code", current_code) \
                .execute()

             if current_code in existing_codes:
                st.error("Product already exists in the same GRN")

             elif existing_db_item.data:
                  st.error("Product already exists in the same GRN")

             else:
                  st.session_state.grn_products.append({
                     "product_code": current_code,
                     "product_name": selected_product_name,
                     "number_of_bags": number_of_bags,
                     "bag_weight": bag_weight,
                     "available_stock": stock_received
                  })

                  st.success("Product added successfully")

         combined_products = []

         if sap_grn_number.strip():
            existing_grn_products = supabase.table("depot_stock") \
               .select("product_code, product_name, number_of_bags, bag_weight, available_stock") \
               .eq("sap_grn_number", sap_grn_number) \
               .execute()

            if existing_grn_products.data:
               combined_products.extend(existing_grn_products.data)

         if st.session_state.grn_products:
            combined_products.extend(st.session_state.grn_products)

         if combined_products:
            st.markdown("### Products in This GRN")
            st.dataframe(combined_products, use_container_width=True)

         if st.button("SAVE GRN", key="save_grn_btn"):
             for item in st.session_state.grn_products:
                 supabase.table("depot_stock").insert({
                    "sap_grn_number": sap_grn_number,
                    "truck_number": truck_number,
                    "depot_code": stock_depot_code,
                    "product_code": item["product_code"],
                    "product_name": item["product_name"],
                    "number_of_bags": item["number_of_bags"],
                    "bag_weight": item["bag_weight"],
                    "available_stock": item["available_stock"],
                    "stock_received_date": str(stock_received_date)
                }).execute()

             st.success("GRN saved successfully")
             st.session_state.grn_products = []


# ================= STOCK LIST =================
      with tab3:
        st.markdown(
            "<h1 style='color:#ED1C24;'>Stock List</h1>",
             unsafe_allow_html=True
        )

        depot_data = supabase.table("depot_master") \
           .select("depot_code") \
           .execute()

        depot_codes = [row["depot_code"] for row in depot_data.data]

        selected_depot = st.selectbox(
             "Depot Code",
             options=depot_codes,
             index=None,
             placeholder="Type to search depot code",
             key="stock_list_depot"
        )

        if selected_depot:
           stock_data = supabase.table("stock_summary_view") \
              .select("*") \
              .eq("depot_code", selected_depot) \
              .execute()

           if stock_data.data:
              summary_data = []

              for row in stock_data.data:
                  total_stock = row["total_stock_mt"]
                  bag_weight = row["bag_weight"] if row["bag_weight"] else 50
                  total_bags = int((total_stock * 1000) / bag_weight)

                  summary_data.append({
                      "Product Name": row["product_name"],
                      "Bag Weight (kg)": bag_weight,
                      "Total Bags": total_bags,
                      "Total Stock (MT)": total_stock
                  })

              st.dataframe(summary_data, use_container_width=True)

              grand_total_stock = sum(
                 row["total_stock_mt"]
                 for row in stock_data.data
             )

              st.success(
                f"Total Available Stock: {grand_total_stock:.2f} MT"
             )

           else:
                st.info("No stock available")
   

   
        # ---------- FUNCTION ----------
      # ---------- FUNCTION ----------
    def get_location_details(address, api_key):
        url = "https://maps.googleapis.com/maps/api/geocode/json"

        params = {
             "address": address.strip(),
             "key": api_key
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data["status"] == "OK":
           result = data["results"][0]
           location = result["geometry"]["location"]

           city = ""
           district = ""
           state = ""
           pincode = ""

           for comp in result["address_components"]:
               types = comp["types"]

               if "locality" in types:
                   city = comp["long_name"]

               if any(t in types for t in [
                    "administrative_area_level_2",
                    "administrative_area_level_3"
               ]):
                    district = comp["long_name"]

               if "administrative_area_level_1" in types:
                   state = comp["long_name"]

               if "postal_code" in types:
                   pincode = comp["long_name"]

           return {
               "latitude": location["lat"],
               "longitude": location["lng"],
               "city": city,
               "district": district,
               "state": state,
               "pincode": pincode
           }

        return None


# ---------- DEALER PAGE ----------
    if selected == "DEALER":
         tab1, tab2, tab3 = st.tabs(["Dealer Entry", "Dealer List","Orders List"])
  
         st.markdown("""
           <style>
            button[data-baseweb="tab"] {
              color: #333333 !important;
              font-weight: 500 !important;
           }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #ED1C24 !important;
                font-weight: 700 !important;
          }
          </style>
          """, unsafe_allow_html=True)

    # ---------- DEALER ENTRY ----------
         with tab1:
            dealer_id = st.text_input("Dealer ID", key="dealer_id")
            dealer_name = st.text_input("Dealer Name", key="dealer_name")
            contact_person = st.text_input("Contact Person", key="dealer_contact")
            mobile = st.text_input("Mobile Number", key="dealer_mobile")
            email = st.text_input("Email", key="dealer_email")
            address = st.text_area("Address", key="dealer_address")
            

            if st.button("Check Location", key="check_location_btn"):
               api_key = "AIzaSyD6kKoeqpSS76MSIg9kREgPsw2j_v1LmDo"

               full_address = address

               location_data = get_location_details(full_address, api_key)

               if not location_data:
                   st.session_state["valid_location"] = False
                   st.error("Invalid address. Please check and try again.")

               else:
                   st.session_state["valid_location"] = True
                   st.session_state["lat"] = location_data["latitude"]
                   st.session_state["lon"] = location_data["longitude"]

        # use separate keys (important)
                   st.session_state["fetched_city"] = location_data["city"]
                   st.session_state["fetched_district"] = location_data["district"]
                   st.session_state["fetched_pincode"] = location_data["pincode"]

                   st.success("Coordinates and location details fetched successfully")

                   st.markdown(
                        "<h2 style='color:#ED1C24;'>Fetched Location Details</h2>",
                         unsafe_allow_html=True
                   )

                   st.markdown(
                       f"""
                       
                       <p style='color:black; font-size:18px;'><b>City:</b> {location_data['city']}</p>
                       <p style='color:black; font-size:18px;'><b>District:</b> {location_data['district']}</p>
                       <p style='color:black; font-size:18px;'><b>Pincode:</b> {location_data['pincode']}</p>
                       <p style='color:black; font-size:18px;'><b>State:</b> {location_data['state']}</p>
                       <p style='color:black; font-size:18px;'><b>Latitude:</b> {location_data['latitude']}</p>
                       <p style='color:black; font-size:18px;'><b>Longitude:</b> {location_data['longitude']}</p>
                       """,
                       unsafe_allow_html=True
                   )
            if st.button("Save Dealer", use_container_width=True, key="save_dealer_btn"):

               if not dealer_id or not dealer_name or not address:
                  st.error("Please fill all mandatory fields")

               elif not st.session_state.get("valid_location", False):
                  st.error("Please check location before saving")

               else:
                   lat = st.session_state["lat"]
                   lon = st.session_state["lon"]

                   try:
                       existing = supabase.table("dealer_master") \
                          .select("*") \
                          .eq("dealer_id", dealer_id) \
                          .execute()

                       if existing.data:
                           st.error("Dealer ID already exists")

                       else:
                          duplicate_location = supabase.table("dealer_master") \
                            .select("*") \
                            .eq("latitude", lat) \
                            .eq("longitude", lon) \
                            .execute()

                          if duplicate_location.data:
                             st.error("Dealer already exists in this location")

                          else:
                              supabase.table("dealer_master").insert({
                                "dealer_id": dealer_id,
                                "dealer_name": dealer_name,
                                "contact_person": contact_person,
                                "mobile": mobile,
                                "email": email,
                                "address": address,
                                "city": st.session_state.get("fetched_city", ""),
                                "district": st.session_state.get("fetched_district", ""),
                                "pincode": st.session_state.get("fetched_pincode", ""),
                                "latitude": lat,
                                "longitude": lon
                              }).execute()

                              st.success("Dealer details saved successfully")

                   except Exception as e:
                       st.error(f"Error: {e}")

    # ---------- DEALER LIST ----------
         with tab2:
            st.markdown("### Saved Dealer Details")

            dealers = supabase.table("dealer_master") \
              .select("*") \
              .execute()

            if dealers.data:
                df = pd.DataFrame(dealers.data)

                search_city = st.text_input(
                    "Search Dealer by City / Pincode",
                     key="search_dealer"
                )

                if search_city:
                   df = df[
                       df["city"].astype(str).str.contains(
                           search_city, case=False, na=False
                       ) |
                       df["pincode"].astype(str).str.contains(
                          search_city, case=False, na=False
                       )
                  ]

                st.dataframe(df, use_container_width=True)

            else:
                st.info("No dealer records found")
         with tab3:
            st.markdown("### Orders List")

            orders = supabase.table("dealer_orders") \
               .select("*") \
               .execute()

            if orders.data:
              df_main = pd.DataFrame(orders.data)

        # 🔽 Create dropdown FIRST
              dealer_ids = sorted(list(set(df_main["dealer_id"])))

              selected_dealer = st.selectbox(
                 "Select Dealer ID",
                  options=dealer_ids,
                  index=None,
                  placeholder="Choose dealer"
              )

        # 🔍 Apply filter AFTER selection
              if selected_dealer:
                 df_main = df_main[
                   df_main["dealer_id"] == selected_dealer
                 ]

        # 📊 Show table
             
              # ---------------- PAGINATION ----------------
              rows_per_page = 10

# Initialize page
              if "order_page" not in st.session_state:
                  st.session_state.order_page = 1

              total_rows = len(df_main)
              total_pages = (total_rows - 1) // rows_per_page + 1

# Slice data
              start = (st.session_state.order_page - 1) * rows_per_page
              end = start + rows_per_page

              paged_df = df_main.iloc[start:end]

# Show table
              st.dataframe(paged_df, use_container_width=True)

# ---------------- NAVIGATION ----------------
              col1, col2, col3 = st.columns([1,2,1])

              with col1:
                st.button(
                  "⬅ Previous",
                   disabled=(st.session_state.order_page == 1),
                   on_click=lambda: (
                       st.session_state.update(order_page=st.session_state.order_page - 1)
                    )
                )

              with col3:
                st.button(
                    "Next ➡",
                    disabled=(st.session_state.order_page == total_pages),
                    on_click=lambda: (
                      st.session_state.update(order_page=st.session_state.order_page + 1)
                    )
                 )

              with col2:
                st.markdown(
                  f"<div style='text-align:center;'>Page {st.session_state.order_page} of {total_pages}</div>",
                  unsafe_allow_html=True
                 )
            else:
               st.info("No orders found")
    if selected == "DASHBOARD":
     st.title("📊 Dashboard")
     
     # 🔥 MOVE THIS ABOVE tab1, tab3, tab4, tab5
     
     tab1, tab3, tab4 = st.tabs([
     "📊 Overall",
     "🏭 Depot",
     "📦 Product"
      ])
         

        
# ---------------- FETCH DATA ----------------

# ---------------- FETCH DATA ----------------
     orders_res = supabase.table("dealer_orders").select("*").execute()
     stock_res = supabase.table("stock_summary_view").select("*").execute()
     dealers_res = supabase.table("dealer_master").select("*").execute()
     allocation_res = supabase.table("order_allocation").select("*").execute()

     df_main = pd.DataFrame(orders_res.data) if orders_res.data else pd.DataFrame()
     df_stock = pd.DataFrame(stock_res.data) if stock_res.data else pd.DataFrame()
     df_dealers = pd.DataFrame(dealers_res.data) if dealers_res.data else pd.DataFrame()
     df_alloc = pd.DataFrame(allocation_res.data) if allocation_res.data else pd.DataFrame()

# ---------------- CLEAN DATA ----------------
     if not df_main.empty:
         df_main["order_date"] = pd.to_datetime(df_main["order_date"])
         df_main["dispatch_time"] = pd.to_datetime(df_main["dispatch_time"])
         df_main["bags"] = pd.to_numeric(df_main["bags"], errors="coerce")

         df_main["processing_time"] = (
             df_main["dispatch_time"] - df_main["order_date"]
         ).dt.total_seconds() / 3600

     with tab1:
# ------------- DATE FILTER ----------------
          
         # Always start fresh
         df = df_main.copy()
         dealer_res = supabase.table("dealer_master").select("dealer_id, city").execute()
         df_dealer = pd.DataFrame(dealer_res.data)

         # ✅ Get only cities that have depots (via orders)

         df_temp = df_main.copy()

# merge dealer to get city
         df_temp = df_temp.merge(df_dealer, on="dealer_id", how="left")

# keep only rows with depot assigned
         df_temp = df_temp.dropna(subset=["assigned_depot"])

# get valid cities
         all_cities = df_temp["city"].dropna().unique()
# ---------------- DATE FILTER ----------------
         st.subheader("📅 Filter by Date")

         df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
         df = df.dropna(subset=["order_date"])

         if df.empty:
             st.warning("No data available")
             st.stop()

         min_date = df["order_date"].min().date()
         max_date = df["order_date"].max().date()

         col1, col2 = st.columns(2)

         with col1:
             start_date = st.date_input("From Date", value=min_date, key="from_tab1")
         with col2:    
             end_date = st.date_input("To Date", value=max_date, key="to_tab1")
        
           
# Apply date filter
         df = df[
             (df["order_date"].dt.date >= start_date) &
             (df["order_date"].dt.date <= end_date)
         ]

# ---------------- CITY FILTER ----------------
         st.subheader("🏙️ Filter by City")

# Merge city
         dealer_res = supabase.table("dealer_master").select("dealer_id, city").execute()
         df_dealer = pd.DataFrame(dealer_res.data)

         df = df.merge(df_dealer, on="dealer_id", how="left")
         df["cluster"] = df["city"]
        

         selected_cities = st.multiselect(
             "Select City",
             options=sorted(all_cities),
             key="city_tab2"
)
# If nothing selected → take all cities
         if not selected_cities:
             selected_cities = list(all_cities)
# 🔥 FIX
         if not selected_cities:
             selected_cities = list(all_cities)

         df = df[df["city"].isin(selected_cities)]
# Top Selling Product (Stock)
         if not df.empty:
             top_product_df = df.groupby("product_name")["bags"].sum().reset_index()
             top_product = top_product_df.sort_values(by="bags", ascending=False).iloc[0]
             top_product_name = top_product["product_name"]
             top_product_value = int(top_product["bags"])
         else:
             top_product_name = "-"
             top_product_value = 0
# ---------------- PLOT CONFIG ----------------
         plot_config = {
             "displayModeBar": True,
             "displaylogo": False
         }
         # ---------------- METRICS (FULLY FILTERED) ----------------
         total_orders = len(df)
         dispatched = len(df[df["status"] == "dispatched"])
         pending = len(df[df["status"] == "pending"])
         total_bags = df["bags"].sum()
         active_dealers = df["dealer_id"].nunique()
         active_depots = df["assigned_depot"].nunique()
         # ✅ NEW (ADD THIS)
         # Get ALL depots for selected cities (not just from orders)

         # ---------------- FINAL STOCK FIX ----------------

# If no city selected → FULL stock
         # ---------------- FINAL STOCK FIX ----------------

# If ALL cities selected → FULL stock
         if set(selected_cities) == set(all_cities):
             total_stock = df_stock["total_stock_mt"].sum()

# If partial selection → filter
         else:
             df_all = df_main.merge(df_dealer, on="dealer_id", how="left")
             df_all = df_all[df_all["city"].isin(selected_cities)]

             all_city_depots = df_all["assigned_depot"].dropna().unique()

             total_stock = df_stock[
                 df_stock["depot_code"].isin(all_city_depots)
             ]["total_stock_mt"].sum()

         efficiency = (dispatched / total_orders * 100) if total_orders > 0 else 0

# ---------------- STOCK (FILTERED BY PRODUCT) ----------------
         # ---------------- STOCK (CITY-BASED CORRECT LOGIC) ----------------

# Step 1: create city-depot mapping from filtered data
         # ---------------- STOCK FIX (IMPORTANT) ----------------

# If no city filter → show full stock (same as Overall)
         
# ---------------- TOP PERFORMERS ----------------

# Top Depot
         if not df.empty:
             top_depot_df = df.groupby("assigned_depot")["bags"].sum().reset_index()
             top_depot = top_depot_df.sort_values(by="bags", ascending=False).iloc[0]
             top_depot_name = top_depot["assigned_depot"]
             top_depot_value = int(top_depot["bags"])
         else:
             top_depot_name = "-"
             top_depot_value = 0

# Top Product
         if not df.empty:
             top_product_df = df.groupby("product_name")["bags"].sum().reset_index()
             top_product = top_product_df.sort_values(by="bags", ascending=False).iloc[0]
             top_product_name = top_product["product_name"]
             top_product_value = int(top_product["bags"])
         else:
             top_product_name = "-"
             top_product_value = 0
# ---------------- UI ----------------
         
         if st.button("🔄 Refresh Data"):
             st.rerun()
         st.subheader("📊 Overall Metrics")
         col1, col2, col3, col4 = st.columns(4)
         col1.metric("📦 Total Orders", total_orders)
         col2.metric("🏭 Total Stock (MT)", f"{total_stock:.2f}")
         col3.metric("👤 Active Dealers", active_dealers)
         col4.metric("🚚 Dispatched", dispatched)

         col5, col6, col7, col8 = st.columns(4)
         col5.metric("⏳ Pending", pending)
         col6.metric("⚡ Efficiency", f"{efficiency:.1f}%")
         col7.metric("📦 Bags", total_bags)
         col8.metric("🏭 Depots", active_depots)

         st.markdown("---")
   
         st.subheader("🏆 Top Performers")

         col9, col10 = st.columns(2)

         col9.metric(
             "🏭 Top Selling Depot",
             top_depot_name,
             f"{top_depot_value} bags"
        )

         col10.metric(
             "📦 Top Selling Product",
             top_product_name,
             f"{top_product_value} bags"
         )
# ---------------- ORDERS BY DEPOT ----------------
         st.subheader("📈 Orders by Depot")

         df_dep = df.groupby("assigned_depot")["bags"].sum().reset_index()

         fig = px.bar(df_dep, x="assigned_depot", y="bags")
         fig.update_yaxes(rangemode="tozero")  # ✅ correct

         st.plotly_chart(fig, use_container_width=True, config=plot_config, key="orders_by_depot")
# ---------------- TREND ----------------
         st.subheader("📈 Orders Trend")

         df["order_day"] = df["order_date"].dt.date

         trend = df.groupby("order_day")["bags"].sum().reset_index()

         fig = px.line(trend, x="order_day", y="bags", markers=True)

         st.plotly_chart(fig, use_container_width=True, config=plot_config, key="orders_trend")
# ---------------- PRODUCT DEMAND ----------------
         st.subheader("📦 Product Demand")

         df_prod = df.groupby("product_name")["bags"].sum().reset_index()

         fig = px.bar(df_prod, x="product_name", y="bags")
         fig.update_yaxes(rangemode="tozero")

         st.plotly_chart(fig, use_container_width=True, config=plot_config, key="product_demand")
        # ---------------- DEPOT COMPARISON ----------------
     

# ---------------- STATUS PIE ----------------
         st.subheader("📊 Order Status Distribution")

         status_counts = df["status"].value_counts().reset_index()
         status_counts.columns = ["status", "count"]

         fig = px.pie(status_counts, names="status", values="count")

         st.plotly_chart(fig, use_container_width=True, config=plot_config, key="status_pie")
# ---------------- TOP DEALERS ----------------
         st.subheader("🏆 Top Dealers")

         top_dealers = (
             df.groupby("dealer_id")["bags"]
             .sum()
             .reset_index()
             .sort_values(by="bags", ascending=False)
             .head(5)
         )

         fig1 = px.bar(top_dealers, x="dealer_id", y="bags")

         st.plotly_chart(
             fig1,
             use_container_width=True,
             config=plot_config,
             key="top_dealers_chart"   # ✅ add key
         )
         st.subheader("📦 Product-wise Available Stock")

         # filter stock based on selected city (via depot)
         # ---------------- PRODUCT STOCK FINAL FIX ----------------

# If ALL cities selected → show FULL stock
         if set(selected_cities) == set(all_cities):
             df_prod_stock = df_stock.groupby("product_name")["total_stock_mt"].sum().reset_index()

# If partial cities → filter
         else:
             df_all = df_main.merge(df_dealer, on="dealer_id", how="left")
             df_all = df_all[df_all["city"].isin(selected_cities)]

             filtered_depots = df_all["assigned_depot"].dropna().unique()

             df_prod_stock = df_stock[
             df_stock["depot_code"].isin(filtered_depots)
             ].groupby("product_name")["total_stock_mt"].sum().reset_index()
         fig2 = px.bar(
             df_prod_stock,
             x="product_name",
             y="total_stock_mt",
             color="product_name"
         )

         fig2.update_layout(
             xaxis_title="Product",
             yaxis_title="Stock (MT)"
         )


         fig2.update_yaxes(rangemode="tozero")  # ✅ correct
         st.plotly_chart(
             fig2,
             use_container_width=True,
             config=plot_config,
             key="product_stock_chart"   # ✅ add key
         )
         # ---------------- MAP ----------------
         # ---------------- MAP (FILTERED) ----------------
         st.subheader("🗺️ Dealer & Depot Locations")

# 🔹 get filtered dealer & depot list
         filtered_dealers = df["dealer_id"].dropna().unique()
         filtered_depots = df["assigned_depot"].dropna().unique()

# 🔹 fetch master data
         dealer_res = supabase.table("dealer_master").select("*").execute()
         df_dealers = pd.DataFrame(dealer_res.data)

         depot_res = supabase.table("depot_master").select("*").execute()
         df_depot = pd.DataFrame(depot_res.data)

# 🔹 FILTER based on selection
         df_dealers = df_dealers[df_dealers["dealer_id"].isin(filtered_dealers)]
         df_depot = df_depot[df_depot["depot_code"].isin(filtered_depots)]

# 🔹 prepare data
         df_dealers = df_dealers.copy()
         df_depot = df_depot.copy()

         df_dealers["type"] = "Dealer"
         df_dealers = df_dealers.rename(columns={"dealer_id": "name"})

         df_depot["type"] = "Depot"
         df_depot = df_depot.rename(columns={"depot_code": "name"})

# 🔹 combine
         df_map = pd.concat([df_dealers, df_depot], ignore_index=True)

# 🔹 clean coordinates
         df_map["latitude"] = pd.to_numeric(df_map["latitude"], errors="coerce")
         df_map["longitude"] = pd.to_numeric(df_map["longitude"], errors="coerce")
         df_map = df_map.dropna(subset=["latitude", "longitude"])

# 🔹 create map
         fig_map = px.scatter_mapbox(
             df_map,
             lat="latitude",
             lon="longitude",
             color="type",
             hover_name="name",
             zoom=6,
             height=500,
             color_discrete_map={
                 "Dealer": "red",
                 "Depot": "blue"
             }
         )

         fig_map.update_traces(marker=dict(size=8, opacity=0.7))

         fig_map.update_layout(
             mapbox_style="open-street-map",
             margin=dict(l=0, r=0, t=0, b=0)
         )

         st.plotly_chart(fig_map, use_container_width=True) 
     def show_depot_dashboard(depot_code, supabase):

         st.title(f"🏭 Depot Dashboard - {depot_code}")
         st.success("Welcome Admin")
    
     with tab3:  
         
         st.subheader("🏭 Select Depot")

         depot_data = supabase.table("depot_master").select("depot_code").execute()
         depot_list = [d["depot_code"] for d in depot_data.data]

         depot_code = st.selectbox("Choose Depot", depot_list)
         
         show_depot_dashboard(depot_code, supabase)
         st.subheader("🏢 Depot Information")

         depot_info = supabase.table("depot_master") \
             .select("depot_code, depot_name, address, city, capacity_mt") \
             .eq("depot_code", depot_code) \
             .single() \
             .execute()

         data = depot_info.data

         if not data:
            st.warning("⚠️ Depot information not available")
         else:
             st.markdown(f"""
             <div style="
                 background:#f8f9fa;
                 padding:15px;
                 border-radius:10px;
                 box-shadow:0 2px 6px rgba(0,0,0,0.05);
             ">
                 <b>🏢 Depot Name:</b> {data.get('depot_name','-')}<br>
                 <b>📍 Address:</b> {data.get('address','-')}<br>
                 <b>🏙 City:</b> {data.get('city','-')}<br>
                 <b>📦 Capacity:</b> {data.get('capacity_mt','-')} MT
             </div>
             """, unsafe_allow_html=True)
                
         st.markdown("---")   # divider line
         st.markdown("<br>", unsafe_allow_html=True)  # space
    # ---------------- STOCK SUMMARY ----------------
         stock_chart_data = supabase.table("stock_summary_view") \
             .select("product_name,total_bags") \
             .eq("depot_code", depot_code) \
             .execute()

         stock_df = pd.DataFrame(stock_chart_data.data)

         if stock_df.empty:
             st.warning("⚠️ No stock data available")
             stock_df = pd.DataFrame(columns=["product_name", "total_bags"])

    # ---------------- STOCK DETAILS ----------------
         stock_details = supabase.table("depot_stock") \
             .select("product_name, number_of_bags, available_stock") \
             .eq("depot_code", depot_code) \
             .execute()

         stock_data = stock_details.data or []

         total_bags_available = sum(int(x["number_of_bags"]) for x in stock_data)
         used_mt = sum(float(x["available_stock"]) for x in stock_data)
 
    # ---------------- DEPOT CAPACITY ----------------
         depot_info = supabase.table("depot_master") \
             .select("capacity_mt") \
             .eq("depot_code", depot_code) \
             .execute()

         capacity_mt = float(depot_info.data[0]["capacity_mt"])
         utilization = (used_mt / capacity_mt) * 100 if capacity_mt > 0 else 0

    # ---------------- ORDER DATA ----------------
         orders = supabase.table("dealer_orders") \
             .select("bags, order_date, product_name") \
             .eq("assigned_depot", depot_code) \
             .execute()

         orders_data = orders.data or []

         total_orders = len(orders_data)
         total_bags_sold = sum(int(x["bags"]) for x in orders_data)

    # ---------------- ACTIVE DAYS ----------------
         if orders_data:
             dates = [pd.to_datetime(x["order_date"]).date() for x in orders_data]
             active_days = (max(dates) - min(dates)).days + 1
         else:
             active_days = 1

         avg_selling_rate = total_bags_sold / active_days if active_days else 0
         avg_order_size = total_bags_sold / total_orders if total_orders else 0

    # ---------------- LOW & DEAD STOCK ----------------
         LOW_STOCK = 300

         low_stock = len(stock_df[stock_df["total_bags"] < LOW_STOCK])

         cutoff = datetime.today().date() - timedelta(days=30)
         recent_products = {
             x["product_name"]
             for x in orders_data
             if pd.to_datetime(x["order_date"]).date() >= cutoff
         }

         dead_stock = len(
             stock_df[~stock_df["product_name"].isin(recent_products)]
         )

    # ---------------- KPI CARDS ----------------
         k1, k2, k3, k4 = st.columns(4)

         def card(title, value, sub=""):
             return f"""
             <div style="padding:15px;border-radius:12px;background:#f5f7fa;text-align:center">
                 <div>{title}</div>
                 <h3>{value}</h3>
                 <div style="color:gray">{sub}</div>
             </div>
             """

         with k1:
             st.markdown(card("📈 Avg Selling Rate", f"{avg_selling_rate:.1f}/day"), unsafe_allow_html=True)

         with k2:
             st.markdown(card("📦 Avg Order Size", f"{avg_order_size:.1f}", "bags/order"), unsafe_allow_html=True)

         with k3:
             st.markdown(card("📉 Dead Stock", dead_stock), unsafe_allow_html=True)

         with k4:
             st.markdown(card("🚨 Low Stock", low_stock), unsafe_allow_html=True)

    # ---------------- STOCK CHART ----------------
         st.subheader("📦 Product-wise Stock")
         LOW_STOCK = 300

# Add color column
         stock_df["color"] = stock_df["total_bags"].apply(
             lambda x: "Low Stock" if x < LOW_STOCK else "Normal"
         )

         fig = px.bar(
             stock_df,
             x="product_name",
             y="total_bags",
             text="total_bags",
             color="color",   # 👈 key line
             color_discrete_map={
                 "Low Stock": "#e74c3c",   # 🔴 red
                 "Normal": "#3498db"       # 🔵 blue
             }
         )

         st.plotly_chart(fig, use_container_width=True)
        
         
    # ---------------- DAYS TO EMPTY ----------------
         st.subheader("⏳ Days to Empty")

         rows = []

         for _, row in stock_df.iterrows():
             name = row["product_name"]
             stock = int(row["total_bags"])

             sales = sum(
                 int(x["bags"])
                 for x in orders_data
                 if x["product_name"].strip().lower() == name.strip().lower()
             )

             avg_daily = sales / active_days if active_days else 0

             if avg_daily == 0:
                 avg_display = "No Sales"
                 days_display = "-"
             else:
                 avg_display = round(avg_daily, 1)
                 days_display = round(stock / avg_daily, 1)

             rows.append([name, stock, avg_display, days_display])

         df_days = pd.DataFrame(rows, columns=[
             "Product", "Stock", "Avg Daily Sales", "Days to Empty"
         ])

         st.dataframe(df_days, use_container_width=True)
         st.subheader("📊 Dealer-wise Orders")

         orders_data = supabase.table("dealer_orders") \
             .select("dealer_id, bags") \
             .eq("assigned_depot", depot_code) \
             .execute()

         df_orders = pd.DataFrame(orders_data.data)

         if df_orders.empty:
             st.warning("⚠️ No dealer orders available")
         else:
            # 🔹 Aggregate total orders per dealer
             dealer_df = df_orders.groupby("dealer_id", as_index=False)["bags"].sum()

            # 🔹 Define threshold
             LOW_ORDER = 200   # change based on your business

            # 🔹 Create color category
             dealer_df["color"] = dealer_df["bags"].apply(
                 lambda x: "Low Orders" if x < LOW_ORDER else "Normal"
             )

            # 🔹 Plot chart
             fig = px.bar(
                 dealer_df,
                 x="dealer_id",
                 y="bags",
                 text="bags",
                 color="color",
                 color_discrete_map={
                     "Low Orders": "#e74c3c",  # red
                     "Normal": "#3498db"       # blue
                 }
             )

             fig.update_layout(
                 xaxis_title="Dealer",
                 yaxis_title="Total Orders (bags)",
                 xaxis_tickangle=-30
             )

             st.plotly_chart(fig, use_container_width=True)        
    # ---------------- UTILIZATION ----------------
         
         st.subheader("🏭 Depot Utilization")

         st.progress(utilization / 100)

         if utilization < 60:
             st.success(f"Healthy: {utilization:.1f}%")
         elif utilization < 85:
             st.warning(f"Moderate: {utilization:.1f}%")
         else:
             st.error(f"Critical: {utilization:.1f}%")
         # ---------------- CAPACITY CARDS ----------------
         available_mt = capacity_mt - used_mt
         utilization = (used_mt / capacity_mt) * 100 if capacity_mt > 0 else 0

         
# 👇 ADD THIS HERE
         if utilization > 85:
             color = "green"
         elif utilization > 60:
             color = "orange"
         else:
             color = "red"
         c1, c2, c3 = st.columns(3)
         
         def metric_card(title, value, sub, icon):
             return f"""
             <div style="
                 padding:18px;
                 border-radius:14px;
                 background:#f5f7fa;
                 box-shadow:0 2px 6px rgba(0,0,0,0.08);
                 text-align:center;
             ">
                 <div style="font-size:18px">{icon} {title}</div>
                 <h2 style="margin:8px 0; color:#1f77b4 !important;">
                 {value}
                 </h2>
                 <div style="color:gray">{sub}</div>
             </div>
             """

         with c1:
             st.markdown(
                 metric_card(
                     "Capacity",
                     f"{capacity_mt:.1f} MT",
                     f"{int(capacity_mt * 20)} bags",  # adjust if needed
                     "🏭"
                 ),
                 unsafe_allow_html=True
             )

         with c2:
             st.markdown(
                 metric_card(
                     "Used",
                     f"{used_mt:.1f} MT",
                     f"{total_bags_available} bags",
                     "📦"
                 ),
                 unsafe_allow_html=True
             )

         with c3:
             st.markdown(
                 metric_card(
                     "Available",
                     f"{available_mt:.1f} MT",
                     f"{int((capacity_mt - used_mt) * 20)} bags",
                     "🟩"
                 ),
                 unsafe_allow_html=True
             )
         # ================= DEPOT STOCK LAYOUT =================

             st.subheader("📦 Depot Stock Layout")

# 🔹 Fetch stock (INCLUDING product)
         stock_data = supabase.table("depot_stock") \
             .select("row_no, column_no, number_of_bags, product_name, sap_grn_number, created_at") \
             .eq("depot_code", depot_code) \
             .execute()


         df = pd.DataFrame(stock_data.data)

         if df.empty:
             st.warning("No stock available")
         else:

    # ---------------- 🔎 FILTER ----------------
             products = df["product_name"].dropna().unique().tolist()
             products.sort()

             selected_product = st.selectbox(
                 "🔎 Filter by Product",
                 ["All"] + products
             )

         full_df = df.copy()   # 🔴 KEEP ORIGINAL

         if selected_product != "All":
             display_df = df[df["product_name"] == selected_product]
         else:
             display_df = df.copy()

         if df.empty:
            st.warning("No stock for selected product")
            st.stop()
         search_grn = st.text_input("🔍 Enter GRN Number")
         if search_grn:

# filter only this GRN from full data
             grn_df = full_df[full_df["sap_grn_number"] == search_grn]

             if grn_df.empty:
                 st.error("❌ No stock found for this GRN")
             else:
                 total_bags = grn_df["number_of_bags"].sum()
                 total_locations = len(grn_df)

                 products = grn_df["product_name"].dropna().unique().tolist()
                 grn_date = grn_df["created_at"].iloc[0]
                 grn_date = pd.to_datetime(grn_date).strftime("%d-%m-%Y %H:%M")
                 st.markdown(f"""
                <div style='
                     background-color:#f4f6f7;
                     padding:15px;
                     border-radius:10px;
                     margin-top:10px;
                 '>
                     <b>📦 GRN Summary</b><br><br>
                     <b>GRN Number:</b> {search_grn} <br>
                     <b>Entry Date:</b> {grn_date} <br>
                     <b>Total Bags:</b> {total_bags} <br>
                     <b>Locations Used:</b> {total_locations} <br>
                     <b>Products:</b> {", ".join(products)}
                 </div>
                 """, unsafe_allow_html=True)

    # ---------------- GRID SIZE ----------------
         depot_info = supabase.table("depot_master") \
             .select("max_rows, max_columns") \
             .eq("depot_code", depot_code) \
             .single() \
             .execute()

         max_row = depot_info.data["max_rows"]
         max_col = depot_info.data["max_columns"]

    # create empty grid
         grid = [[None for _ in range(max_col)] for _ in range(max_row)]

    # fill grid
         for _, r in display_df.iterrows():
             row = int(r["row_no"]) - 1
             col = int(r["column_no"]) - 1

             if grid[row][col] is None:
                 grid[row][col] = {
                     "stock": []
                 }

             grid[row][col]["stock"].append({
                 "bags": int(r["number_of_bags"]),
                 "product": r["product_name"],
                 "grn": r["sap_grn_number"]
             })

    # ---------------- DISPLAY GRID ----------------
         for i in range(max_row):
             st.markdown(f"**Row {i+1}**")
             cols = st.columns(max_col)

             for j in range(max_col):

                 cell = grid[i][j]

                 if cell is None:
                     total_bags = 0
                     grn_bags = 0
                 else:
                     stock_list = cell["stock"]

                     total_bags = sum(item["bags"] for item in stock_list)

                     if search_grn:
                         grn_bags = sum(
                             item["bags"] for item in stock_list
                             if item["grn"] == search_grn
                         )
                     else:
                         grn_bags = total_bags
  
            # 🎨 Color logic
                 bags_to_show = grn_bags if search_grn else total_bags

                 if search_grn:
                     if grn_bags > 0:
                          color = "#3498db"  # 🔵 highlight GRN match
                     else:
                         color = "#ecf0f1"  # faded
                 else:
                     if total_bags == 0:
                         color = "#ff4b4b"
                     elif total_bags < 10:
                         color = "#ffa500"
                     else:
                         color = "#2ecc71"

            

                 cols[j].markdown(f"""
                     <div style='
                         background-color:{color};
                         width:70px;
                         height:80px;
                         min-width:70px;
                         min-height:80px;
                         max-width:70px;
                         max-height:80px;
                         border-radius:10px;
                         text-align:center;
                         color:white;
                         display:flex;
                         flex-direction:column;
                         justify-content:center;
                         align-items:center;
                         margin:auto;
                         box-sizing:border-box;
                     '>
                         <div style="font-size:10px;">R{i+1}-C{j+1}</div>
                         <div style="font-size:18px; font-weight:bold;">{bags_to_show}</div>
                     </div>
                     """, unsafe_allow_html=True)
                 df_layout = pd.DataFrame(stock_data.data)
     with tab4:   # 📦 Product tab (IMPORTANT)

         st.subheader("📦 Product Dashboard")

        # ---------------- FETCH STOCK ----------------
         stock_res = supabase.table("depot_stock") \
             .select("product_name, number_of_bags, depot_code, created_at") \
             .execute()

         df = pd.DataFrame(stock_res.data)

# ---------------- CLEAN DATA ----------------
         df['bags'] = pd.to_numeric(df['number_of_bags'], errors='coerce')
         df['depot'] = df['depot_code']

# ---------------- DATE FILTER ----------------
         # ---------------- DATE FILTER (CUSTOM UI) ----------------
         st.subheader("📅 Filter by Date")

         col1, col2 = st.columns(2)

         with col1:
             from_date = st.date_input("From Date")

         with col2:
             to_date = st.date_input("To Date")

# Apply filter
         if 'created_at' in df.columns:

             df['date'] = pd.to_datetime(df['created_at'], errors='coerce')

             if from_date and to_date:
                 df = df[
                     (df['date'] >= pd.to_datetime(from_date)) &
                     (df['date'] <= pd.to_datetime(to_date))
        ]
        # ---------------- PRODUCT FILTER ----------------
         product_list = df['product_name'].dropna().unique().tolist()
         product_list.sort()

         selected_product = st.selectbox("Select Product", product_list)

         product_df = df[df['product_name'] == selected_product]

         if product_df.empty:
             st.warning("No data for selected product")
             st.stop()
        
        # ---------------- KPI ----------------
         total_stock = product_df['bags'].sum()
         total_depots = product_df['depot'].nunique()

         col1, col2 = st.columns(2)

         col1.metric("📦 Total Stock", int(total_stock))
         col2.metric("🏭 Depots", total_depots)

         # ---------------- CHART ----------------
         st.subheader("🏭 Stock by Depot")

         depot_stock = (
             product_df.groupby('depot')['bags']
             .sum()
             .reset_index()
         )

         fig = px.bar(
             depot_stock,
             x='depot',
             y='bags',
             text='bags'
         )

         st.plotly_chart(fig, use_container_width=True)
         avg_stock = total_stock / total_depots if total_depots else 0
         highest = depot_stock.loc[depot_stock['bags'].idxmax()]
         lowest = depot_stock.loc[depot_stock['bags'].idxmin()]
         LOW_LIMIT = 300

         low_stock_count = len(depot_stock[depot_stock['bags'] < LOW_LIMIT])
         top_share = (highest['bags'] / total_stock) * 100 if total_stock else 0
         # ---------------- FETCH SALES ----------------
         orders = supabase.table("dealer_orders") \
             .select("bags, assigned_depot, product_name") \
             .execute()

         orders_df = pd.DataFrame(orders.data)

         if not orders_df.empty:
             orders_df['bags'] = pd.to_numeric(orders_df['bags'], errors='coerce')
             orders_df = orders_df[orders_df['product_name'] == selected_product]
         sales_depot = (
             orders_df.groupby('assigned_depot')['bags']
             .sum()
             .reset_index()
         )
         
    # Filter same product
             
         col1, col2, col3, col4 = st.columns(4)

         col1.metric("📊 Avg Stock / Depot", int(avg_stock))
         if not sales_depot.empty:

              top_selling = sales_depot.loc[sales_depot['bags'].idxmax()]
              low_selling = sales_depot.loc[sales_depot['bags'].idxmin()]
              col2.metric("" \
                     "🏆 Top Selling Depot",
                     top_selling['assigned_depot'],
                     f"{int(top_selling['bags'])} bags"
              )
              col3.metric(
                 "📉 Lowest Selling Depot",
                 low_selling['assigned_depot'],
                 f"{int(low_selling['bags'])} bags"
             )
         else:
             col2.metric("🏆 Top Selling Depot", "No Data", "-")
             col3.metric("📉 Lowest Selling Depot", "No Data", "-")
         col4.metric("📦 Concentration", f"{top_share:.1f}%")
         st.subheader("📈 Sales Trend (Depot-wise)")

# ---------------- FETCH DATA ----------------
         orders = supabase.table("dealer_orders") \
             .select("bags, order_date, assigned_depot, product_name") \
             .execute()

         orders_df = pd.DataFrame(orders.data)

         if orders_df.empty:
             st.warning("No sales data available")
         else:

            # ---------------- CLEAN ----------------
             orders_df['bags'] = pd.to_numeric(orders_df['bags'], errors='coerce')
             orders_df['date'] = pd.to_datetime(orders_df['order_date'], errors='coerce')

            # ---------------- FILTER PRODUCT ----------------
             orders_df = orders_df[orders_df['product_name'] == selected_product]

             if orders_df.empty:
                st.info("No sales for selected product")
             else:

                # ---------------- GROUP ----------------
                 trend = (
                     orders_df.groupby(['date', 'assigned_depot'])['bags']
                     .sum()
                     .reset_index()
                )

                # ---------------- INTERACTIVE CHART ----------------
                 fig = px.line(
                     trend,
                     x='date',
                     y='bags',
                     color='assigned_depot',   # 🔥 THIS MAKES FILTER INSIDE CHART
                     markers=True,
                     title="Depot-wise Sales Trend"
                 )

                 st.plotly_chart(fig, use_container_width=True)
    # ---------------- MONITOR PAGE ----------------
    elif selected == "MONITOR":

    # ---------- TAB STYLE ----------
        st.markdown("""
        <style>
        button[data-baseweb="tab"] {
            color: #333 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            background: none !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ED1C24 !important;
            border-bottom: 2px solid #ED1C24 !important;
        }
        
       
        </style>
        """, unsafe_allow_html=True)
        
        # ---------- TEXT TABS ----------
        tab1, tab2, tab3 = st.tabs(["Damage", "Attendance", "CCTV"])

        # 🚨 DAMAGE
        with tab1:
            st.title("🧑‍💼 Damage Approval")

# -------- FETCH PENDING REQUESTS --------
            def get_requests():
                return supabase.table("damage_requests") \
                    .select("*") \
                    .eq("status", "pending") \
                    .execute().data

            data = get_requests()
            data = [req for req in data if req["status"] == "pending"]
            if not data:
                st.success("✅ No pending requests")

            else:
                for req in data:

                    st.markdown("---")

                    st.write(f"📦 Product: {req['product_name']} ({req['product_id']})")
                    st.write(f"🏭 Depot: {req['depot_id']}")
                    st.write(f"🔢 Qty: {req['quantity']}")
                    st.write(f"⚠️ Type: {req['damage_type']}")
                    st.write(f"📝 Remarks: {req['remarks']}")

                    col1, col2 = st.columns(2)

                    # -------- APPROVE --------
                    with col1:
                        if st.button("✅ Approve", key=f"approve_{req['id']}", type="secondary"):
                            try:
                                depot_id = req["depot_id"]
                                product_id = req["product_id"]

                                # 🔹 STEP 1: Fetch stock FIRST
                                stock = supabase.table("depot_stock") \
                                    .select("*") \
                                    .eq("product_code", product_id) \
                                    .eq("depot_code", depot_id) \
                                    .eq("row_no", req["row_no"]) \
                                    .eq("column_no", req["column_no"]) \
                                    .execute().data[0]

                                # 🔹 STEP 2: Validate
                                if req["quantity"] > stock["number_of_bags"]:
                                    st.error("❌ Not enough stock")
                                    st.stop()

                                # 🔹 STEP 3: Update stock
                                new_good = stock["number_of_bags"] - req["quantity"]
                                new_damaged = stock["damaged_bags"] + req["quantity"]

                                supabase.table("depot_stock").update({
                                    "number_of_bags": new_good,
                                    "damaged_bags": new_damaged
                                }).eq("product_code", product_id) \
                                .eq("depot_code", depot_id) \
                                .eq("row_no", req["row_no"]) \
                                .eq("column_no", req["column_no"]) \
                                .execute()

                                # 🔹 STEP 4: Update request (ONLY ONCE, at END)
                                res = supabase.table("damage_requests").update({
                                    "status": "approved"
                                }).eq("id", req["id"]).execute()

                                # 🔹 DEBUG (temporary)
                                st.write(res)

                                st.success("✅ Approved")
                                st.rerun()

                            except Exception as e:
                                st.error(f"Error: {e}")

                    # -------- REJECT --------
                    with col2:
                        if st.button("❌ Reject", key=f"reject_{req['id']}", type="secondary"):
                            supabase.table("damage_requests").update({
                                "status": "rejected"
                            }).eq("id", req["id"]).execute()

                            st.warning("❌ Rejected")
                            st.rerun()
            st.markdown("---")
            st.subheader("📊 Approved Damage (Stock Cleared)")

            # 🔹 Get depot list
            depots = supabase.table("depot_master").select("depot_code").execute().data
            depot_list = [d["depot_code"] for d in depots]

            # 🔹 Dropdown filter
            depot_filter = st.selectbox("Select Depot", ["All"] + depot_list)

            # 🔹 STEP 1: DEFINE QUERY FIRST
            query = supabase.table("damage_requests") \
                .select("*") \
                .eq("status", "approved")

            # 🔹 STEP 2: APPLY FILTER
            if depot_filter != "All":
                query = query.eq("depot_id", depot_filter)

            # 🔹 STEP 3: EXECUTE
            approved_data = query.execute().data

            # 🔹 DISPLAY
            if not approved_data:
                st.info("No approved damage records")

            else:
                for req in approved_data:
                    st.markdown("---")

                    st.write(f"📦 Product: {req['product_name']} ({req['product_id']})")
                    st.write(f"🏭 Depot: {req['depot_id']}")
                    st.write(f"🔢 Qty: {req['quantity']}")
                    st.write(f"⚠️ Type: {req['damage_type']}")
                    st.write(f"📝 Remarks: {req['remarks']}")
                    st.write(f"📅 Date: {req['created_at']}")
                    col1, col2 = st.columns(2)

    # 🗑️ DISPOSE BUTTON
                    with col2:
                        if st.button("🗑️ Dispose", key=f"dispose_{req['id']}", type="secondary"):
                            try:
                                depot_id = req["depot_id"]
                                product_id = req["product_id"]

                                # 🔹 Fetch stock
                                stock = supabase.table("depot_stock") \
                                    .select("*") \
                                    .eq("product_code", product_id) \
                                    .eq("depot_code", depot_id) \
                                    .eq("row_no", req["row_no"]) \
                                    .eq("column_no", req["column_no"]) \
                                    .execute().data[0]

                                # 🔹 Validate
                                if req["quantity"] > stock["damaged_bags"]:
                                    st.error("❌ Not enough damaged stock")
                                    st.stop()

                                # 🔹 Update damaged stock
                                new_damaged = stock["damaged_bags"] - req["quantity"]

                                supabase.table("depot_stock").update({
                                    "damaged_bags": new_damaged
                                }).eq("product_code", product_id) \
                                .eq("depot_code", depot_id) \
                                .eq("row_no", req["row_no"]) \
                                .eq("column_no", req["column_no"]) \
                                .execute()

                                # 🔹 Update request status → disposed
                                supabase.table("damage_requests").update({
                                    "status": "disposed"
                                }).eq("id", req["id"]).execute()

                                st.success("🗑️ Disposed successfully")
                                st.rerun()

                            except Exception as e:
                                st.error(f"Error: {e}")
        # 🧑 ATTENDANCE
        with tab2:
            

           
            import pandas as pd
            import math

            st.markdown("### 📍 Live Employee Tracking + Attendance")

            # -------- FETCH DEPOT LIST --------
            depot_res = supabase.table("depot_master") \
                .select("depot_code, latitude, longitude") \
                .execute()

            depot_list = depot_res.data

            if not depot_list:
                st.error("No depot data found")
                st.stop()

            depot_codes = [d["depot_code"] for d in depot_list]

            # -------- SELECT DEPOT --------
            DEPOT_ID = st.selectbox("🏭 Select Depot", depot_codes)

            # get selected depot lat/lon
            depot_data = next(d for d in depot_list if d["depot_code"] == DEPOT_ID)
            depot_lat = float(depot_data["latitude"])
            depot_lon = float(depot_data["longitude"])

            st.info(f"📌 Depot Location: {depot_lat}, {depot_lon}")

            # -------- FETCH EMPLOYEE LOCATIONS --------
            res = supabase.table("employee_location") \
                .select("emp_id, latitude, longitude, updated_at") \
                .eq("depot_code", DEPOT_ID) \
                .order("updated_at", desc=True) \
                .execute()

            data = res.data

            if not data:
                st.warning("No employee data")
                st.stop()

            df = pd.DataFrame(data)

            # latest per employee
            df = df.sort_values("updated_at", ascending=False) \
                .drop_duplicates(subset=["emp_id"])

            # -------- DISTANCE FUNCTION --------
            def calculate_distance(lat1, lon1, lat2, lon2):
                R = 6371  # km

                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)

                a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
                    math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

                c = 2 * math.asin(math.sqrt(a))
                return R * c  # km

            # -------- CHECK NEAR/FAR --------
            THRESHOLD_KM = 0.5   # 👈 500 meters

            status_list = []
            distance_list = []

            for _, row in df.iterrows():

                emp_lat = float(row["latitude"])
                emp_lon = float(row["longitude"])

                dist = calculate_distance(depot_lat, depot_lon, emp_lat, emp_lon)

                distance_list.append(round(dist, 3))

                if dist <= THRESHOLD_KM:
                    status_list.append("🟢 Present")
                else:
                    status_list.append("🔴 Not Present")

            df["distance_km"] = distance_list
            df["status"] = status_list

            # rename for map
            map_df = df.rename(columns={"latitude": "lat", "longitude": "lon"})

            # -------- MAP --------
            st.map(map_df)

            # -------- RESULT --------
            st.markdown("### 👨‍🏭 Attendance Status")
            st.dataframe(df, use_container_width=True)

            # -------- SUMMARY --------
            present_count = df[df["status"] == "🟢 Present"].shape[0]
            total = len(df)

            st.success(f"Present: {present_count} / {total}")
        # 📷 CCTV
        with tab3:
            st.markdown("### CCTV Monitoring")
            st.text_input("Camera URL")