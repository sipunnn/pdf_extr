##from cv2 import split
import pdfplumber
import os
import re
from pdf_parser import data_extractor_alphanumeric,data_extractor_numbers,data_extractor_string
from datetime import datetime
import psycopg2

##conn= psycopg2.connect(database="Bill_of_lading", user='postgres',password='shubham1',host='localhost',port='5432')
##cursor=conn.cursor()

All_data = {}
l = ['(',')','.','/','-',',','%','@',"'",'*',':','\n']

path = r"D:\extract_pdf"
os.chdir(path)

def BL_Extraction(path,file_name):
    
    with pdfplumber.open(path)as pdf:
        pages = pdf.pages
        text_all = ''
        for page in pages:
            text = page.extract_text()
            text_all += text
        text_alll = text_all.lower().lstrip().rstrip()
        print(text_alll)

        ## BL NO 
        data_extractor_alphanumeric(text_alll,'shipper',1,All_data,'consignee','BL_No',l,'\w{7}\d{7}|\w{4}\d{10}|\w+\/\w+\/\d{5}',0)
        if All_data['BL_No']==0:
            data_extractor_alphanumeric(text_alll,'b/l no.',1,All_data,'shipper','BL_No',l,'\d{9}',0)
        
        ## BD DATE

        data_extractor_alphanumeric(text_alll,'on board',1,All_data,'sign','BL_Date',l,'\d{4}\-\d+\-\d+|\d+\-\w+\-\d+|\d+\s\w+\s\d+',0)
        if All_data['BL_Date']==0:
            data_extractor_alphanumeric(text_alll,'signature',1,All_data,'culines isa','BL_Date',l,'\d+\-\w+\-\d+',0)
        if All_data['BL_Date']==0:
            data_extractor_alphanumeric(text_alll,'date of issue',1,All_data,'destination','BL_Date',l,'\d+\-[a-z]+\-[0-9]+',0)
       

        ## SHIPPER

        data_extractor_alphanumeric(text_alll,'booking no.',1,All_data,'tel:','Shipper',l,'\w+\s\w+\,\s\w+',0)
        if All_data['Shipper']==0:
            data_extractor_alphanumeric(text_alll,'booking no.',1,All_data,'(as shipper','Shipper',l,'\w+\s\w+\s\w+\s\w+',0)
        if All_data['Shipper']==0:
            data_extractor_alphanumeric(text_alll,'waybill no.',1,All_data,'address:','Shipper',l,'\w+\s\w+\s\w+\.\s\w+',0)
        if All_data['Shipper']==0:
            data_extractor_alphanumeric(text_alll,'sea waybill no.',1,All_data,'technology','Shipper',l,'[a-z]+\s[a-z]+\s[a-z]+',0)
        if All_data['Shipper']==0:
            data_extractor_alphanumeric(text_alll,'shipper',1,All_data,'technology','Shipper',l,'[a-z]+\s[a-z]+\s[a-z]+',0)
        if All_data['Shipper']==0:
            data_extractor_alphanumeric(text_alll,'shipper',1,All_data,'projects','Shipper',l,'\w+\-\w+\s\w+',0)
        if All_data['Shipper']==0:
            data_extractor_alphanumeric(text_alll,'b l no.',1,All_data,'reference','Shipper',l,'[a-z]+\s[a-z]+',0)
        
        
        ##SHIPPER COUNTRY

        print(text_alll)
        data_extractor_alphanumeric(text_alll,'hs code',1,All_data,'**iec','Shipper_Country',l,'china',0)
        if All_data['Shipper_Country']==0:
            data_extractor_alphanumeric(text_alll,'booking no.',1,All_data,'onward inland','Shipper_Country',l,'stafford|glenview',0)
        if All_data['Shipper_Country']==0:
            data_extractor_alphanumeric(text_alll,'development',1,All_data,'consignee','Shipper_Country',l,'china',0)
        if All_data['Shipper_Country'] == 0:
            data_extractor_alphanumeric(text_alll,'bill of lading',1,All_data,'consignee','Shipper_Country',l,'germany',0)


        ##CONSIGNEE

        data_extractor_alphanumeric(text_alll,'ltd.',1,All_data,'add:','Consignee',l,'[a-z]+\s[a-z]+\s[a-z]+',0)
        if All_data['Consignee']==0:
            data_extractor_alphanumeric(text_alll,'(see clause 22)',1,All_data,'same as consginee','Consignee',l,'[a-z]+\s[a-z]+',0)
        if All_data['Consignee']==0:
            data_extractor_alphanumeric(text_alll,'(see clause 22)',1,All_data,'same as consignee','Consignee',l,'\w+\s\w+\s\w+\s\w+',0)
        if All_data['Consignee']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'fmc/chb no.','Consignee',l,'\w{3}\s\w+\s\w+\s\w+\.\s\w+\.',0)
        if All_data['Consignee']==0:
            data_extractor_alphanumeric(text_alll,'and references',1,All_data,'solutions','Consignee',l,'[a-z]+\s[a-z]+\si\w+',0)
        if All_data['Consignee']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'p-21, kubera','Consignee',l,'\w+\s\w+\sn\w+',0)
        if All_data['Consignee']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'2/2 basement','Consignee',l,'[a-z]+\s[a-z]+\s[a-z]+\s[a-z]+',0)

        ##CONSIGNEE ADDRESS 1

        data_extractor_alphanumeric(text_alll,'add:',1,All_data,'opp.','Consignee_Address_1',l,'\w+\s\w+\,\s\w+\s\w+\s\d+\,\s\w+\s\w+\s\w+',0)
        if All_data['Consignee_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'same as consignee',1,All_data,'iec','Consignee_Address_1',l,'\w+\s\w+\:\s\d+\w\s\w+\s\d+\s\w\,\s\w+\s\w+\-\sii',0)
        if All_data['Consignee_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'kd overseas',1,All_data,'iec','Consignee_Address_1',l,'\d+\s[a-z]+\s[a-z]+\,',0)
        if All_data['Consignee_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'fmc/chb no.',1,All_data,'hirachand','Consignee_Address_1',l,'[0-9,]+\s[a-z]+\s[a-z,]+\s[a-z]+',0)
        if All_data['Consignee_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Consignee_Address_1',l,'[0-9-,]+\s[a-z]+\s[a-z]+\,|\w\-\d+\,+\s[a-z]+\s[a-z]+\s[a-z,]+\s[a-z.]+\s\w+\,|\d\/\d\s\w+\s\w+',0)


        ##CONSIGNEE ADDRESS 2

        data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'received','Consignee_Address_2',l,'\w+\.\w+\s\w+\,\s\w+\s\w+\s\w+',0)
        if All_data['Consignee_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'part- ii',1,All_data,'haridwar,','Consignee_Address_2',l,'[a-z]+\s[a-z]+\s[a-z]+\,',0)
        if All_data['Consignee_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'iec:',1,All_data,'pan:','Consignee_Address_2',l,'[a-z\/]+\s\w+\s\w+\,\s[a-z]+\s\w+\,\s\w+',0)
        if All_data['Consignee_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'fmc/chb no.',1,All_data,'estate','Consignee_Address_2',l,'[a-z]+\s[a-z]+\s[a-z]+',0)
        if All_data['Consignee_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'solutions',1,All_data,'point and country','Consignee_Address_2',l,'\w+\s\w+\,\s\w+\,',0)
        if All_data['Consignee_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Consignee_Address_2',l,'[a-z]+\s\w+\-\w+\s\w+\,\s\w+\,|\w+\s\d+\s[a-z]+\s[a-z]+',0)

        ##CONSIGNEE ADDRESS 3

        data_extractor_alphanumeric(text_alll,'container(s',1,All_data,'package(s)','Consignee_Address_3',l,'\w+\s\w+\s\d\,\w+\s+\w+',0)
        if All_data['Consignee_Address_3']==0:
            data_extractor_alphanumeric(text_alll,'notify',1,All_data,'vessel','Consignee_Address_3',l,'[a-z]+\,+\s[a-z]+\s\-\s\d+\s\w+|\w+\-\d+\,\s\w+\s\,\s\w+',0)
        if All_data['Consignee_Address_3']==0:
            data_extractor_alphanumeric(text_alll,'sarvapriya',1,All_data,'prism global','Consignee_Address_3',l,'\.\s\w+',0)
        if All_data['Consignee_Address_3']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Consignee_Address_3',l,'[a-z]+\s[a-z]+\s\d+|\w+\s\w+\,\si\w+|\w+\-\d+\,\s\w+\,\s\w+',0)
       

        ##CONSIGNEE COUNTRY


        data_extractor_alphanumeric(text_alll,'rajkot',1,All_data,'loading','Consignee_Country',l,'india',0)
        if All_data['Consignee_Country']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'vessel','Consignee_Country',l,'india',0)
        if All_data['Consignee_Country']==0:
            data_extractor_alphanumeric(text_alll,'part- ii',1,All_data,'iec no.:','Consignee_Country',l,'india',0)
        if All_data['Consignee_Country']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Consignee_Country',l,'india',0)


        ##CONSIGNEE IEC NO

        data_extractor_alphanumeric(text_alll,'iec',1,All_data,'pan','Cnee_IEC_No',l,'[a-z0-9]{10}|a-z|\d{10}',0)
        if All_data['Cnee_IEC_No']==0:
            data_extractor_alphanumeric(text_alll,'ie code:',1,All_data,'email','Cnee_IEC_No',l,'[a-z0-9]{10}',0)
        if All_data['Cnee_IEC_No']==0:
            data_extractor_alphanumeric(text_alll,'iec code',1,All_data,'\n','Cnee_IEC_No',l,'[a-z0-9]{10}',0)


        ##CONSIGNEE PAN NO
        
        data_extractor_alphanumeric(text_alll,'pan',1,All_data,'copy','Cnee_PAN_No.',l,'[a-z0-9]{10}',0)
        if All_data['Cnee_PAN_No.']==0:
            data_extractor_alphanumeric(text_alll,'pan',1,All_data,'vessel','Cnee_PAN_No.',l,'[a-z0-9]{10}',0)
        if All_data['Cnee_PAN_No.']==0:
            data_extractor_alphanumeric(text_alll,'pan',1,All_data,'\n','Cnee_PAN_No.',l,'[a-z0-9]{10}',0)


        ##CONSIGNEE GST_NO

        data_extractor_alphanumeric(text_alll,'gst',1,All_data,'notify','Cnee_GST_No.',l,'\d+\w+',0)
        if All_data['Cnee_GST_No.']==0:
            data_extractor_alphanumeric(text_alll,'gst',1,All_data,'.com','Cnee_GST_No.',l,'\d+\w+',0)
        if All_data['Cnee_GST_No.']==0:
            data_extractor_alphanumeric(text_alll,'gstn',1,All_data,'\n','Cnee_GST_No.',l,'\d+\w+',0)


        ##CONSIGNEE EMAIL ID
        email=''
        try:
            emai = re.search(r"(?s)mail.*?.com",text_alll).group()
            email = re.sub(r"mail\s\-|mail\sid\:|mail\:|9\,\srex\schambers\,\swalchand|mail\s|id\s\:|\n|\s\s",'',emai)
        except:
            pass
        # print(email)
        All_data['Cnee_Email_Id'] = email

        ##NOTIFY PARTY

        data_extractor_alphanumeric(text_alll,'ltd.',1,All_data,'add:','Notify_Party',l,'[a-z]+\s[a-z]+\s[a-z]+',0)
        if All_data['Notify_Party']==0:
            data_extractor_alphanumeric(text_alll,'(see clause 22)',1,All_data,'same as consginee','Notify_Party',l,'[a-z]+\s[a-z]+',0)
        if All_data['Notify_Party']==0:
            data_extractor_alphanumeric(text_alll,'(see clause 22)',1,All_data,'same as consignee','Notify_Party',l,'\w+\s\w+\s\w+\s\w+',0)
        if All_data['Notify_Party']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'fmc/chb no.','Notify_Party',l,'\w{3}\s\w+\s\w+\s\w+\.\s\w+\.',0)
        if All_data['Notify_Party']==0:
            data_extractor_alphanumeric(text_alll,'and references',1,All_data,'solutions','Notify_Party',l,'[a-z]+\s[a-z]+\si\w+',0)
        if All_data['Notify_Party']==0:
            data_extractor_alphanumeric(text_alll,'notify address',1,All_data,'delivery','Notify_Party',l,'d\w+\s\w+\s\w+\.\s\w+\.',0)
        if All_data['Notify_Party']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'2/2 basement','Notify_Party',l,'[a-z]+\s[a-z]+\s[a-z]+\s[a-z]+',0)

        
        ##NOTIFY ADDRESS 1

        data_extractor_alphanumeric(text_alll,'add:',1,All_data,'opp.','Notify_Party_Address_1',l,'\w+\s\w+\,\s\w+\s\w+\s\d+\,\s\w+\s\w+\s\w+',0)
        if All_data['Notify_Party_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'same as consignee',1,All_data,'iec','Notify_Party_Address_1',l,'\w+\s\w+\:\s\d+\w\s\w+\s\d+\s\w\,\s\w+\s\w+\-\sii',0)
        if All_data['Notify_Party_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'kd overseas',1,All_data,'iec','Notify_Party_Address_1',l,'\d+\s[a-z]+\s[a-z]+\,',0)
        if All_data['Notify_Party_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'fmc/chb no.',1,All_data,'hirachand','Notify_Party_Address_1',l,'[0-9,]+\s[a-z]+\s[a-z,]+\s[a-z]+',0)
        if All_data['Notify_Party_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'notify address',1,All_data,'pre-carriage','Notify_Party_Address_1',l,'\d+\,\s\w+\s\w+\s\w+',0)
        if All_data['Notify_Party_Address_1']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Notify_Party_Address_1',l,'[0-9-,]+\s[a-z]+\s[a-z]+\,|\d\/\d\s\w+\s\w+',0)
            


        ##NOTIFY ADDRESS 2

        data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'received','Notify_Party_Address_2',l,'\w+\.\w+\s\w+\,\s\w+\s\w+\s\w+',0)
        if All_data['Notify_Party_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'part- ii',1,All_data,'haridwar,','Notify_Party_Address_2',l,'[a-z]+\s[a-z]+\s[a-z]+\,',0)
        if All_data['Notify_Party_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'iec:',1,All_data,'pan:','Notify_Party_Address_2',l,'[a-z\/]+\s\w+\s\w+\,\s[a-z]+\s\w+\,\s\w+',0)
        if All_data['Notify_Party_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'fmc/chb no.',1,All_data,'estate','Notify_Party_Address_2',l,'[a-z]+\s[a-z]+\s[a-z]+',0)
        if All_data['Notify_Party_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'solutions',1,All_data,'point and country','Notify_Party_Address_2',l,'\w+\s\w+\,\s\w+\,',0)
        if All_data['Notify_Party_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'notify address',1,All_data,'pre-carriage','Notify_Party_Address_2',l,'\d\w+\s\w+\,\s\w+\s\w+\s\w+\,\s\w+\s\w+\,|\d\w+\s\w+\,\s\w+\s.*?india',0)
        if All_data['Notify_Party_Address_2']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Notify_Party_Address_2',l,'\w+\s\d+\s[a-z]+\s[a-z]+',0)


        ##NOTIFY ADDRESS 3

        data_extractor_alphanumeric(text_alll,'container(s',1,All_data,'package(s)','Notify_Party_Address_3',l,'\w+\s\w+\s\d\,\w+\s+\w+',0)
        if All_data['Notify_Party_Address_3']==0:
            data_extractor_alphanumeric(text_alll,'notify',1,All_data,'vessel','Notify_Party_Address_3',l,'[a-z]+\,+\s[a-z]+\s\-\s\d+\s\w+|\w+\-\d+\,\s\w+\s\,\s\w+',0)
        if All_data['Notify_Party_Address_3']==0:
            data_extractor_alphanumeric(text_alll,'sarvapriya',1,All_data,'prism global','Notify_Party_Address_3',l,'\.\s\w+',0)
        if All_data['Notify_Party_Address_3']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Notify_Party_Address_3',l,'[a-z]+\s[a-z]+\s\d+|\w+\s\w+\,\si\w+',0)
        if All_data['Notify_Party_Address_3']==0:
            data_extractor_alphanumeric(text_alll,'notify address',1,All_data,'pre-carriage','Notify_Party_Address_3',l,'\w\.\w\.\w\.\w+\,\s\w+\s\(\w\)',0)


        ##NOTIFY COUNTRY

        data_extractor_alphanumeric(text_alll,'rajkot',1,All_data,'loading','Notify_Country',l,'india',0)
        if All_data['Notify_Country']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'vessel','Notify_Country',l,'india',0)
        if All_data['Notify_Country']==0:
            data_extractor_alphanumeric(text_alll,'part- ii',1,All_data,'iec no.:','Notify_Country',l,'india',0)
        if All_data['Notify_Country']==0:
            data_extractor_alphanumeric(text_alll,'consignee',1,All_data,'notify','Notify_Country',l,'india',0)


        ##NOTIFY IEC NO

        data_extractor_alphanumeric(text_alll,'iec',1,All_data,'pan','Ntfy_IEC_No.',l,'[a-z0-9]{10}|a-z|\d{10}',0)
        if All_data['Ntfy_IEC_No.']==0:
            data_extractor_alphanumeric(text_alll,'ie code:',1,All_data,'email','Ntfy_IEC_No.',l,'[a-z0-9]{10}',0)
        if All_data['Ntfy_IEC_No.']==0:
            data_extractor_alphanumeric(text_alll,'iec code',1,All_data,'\n','Ntfy_IEC_No.',l,'[a-z0-9]{10}',0)


        ##NOTIFY PAN NO

        data_extractor_alphanumeric(text_alll,'pan',1,All_data,'copy','Ntfy_PAN_No.',l,'[a-z0-9]{10}',0)
        if All_data['Ntfy_PAN_No.']==0:
            data_extractor_alphanumeric(text_alll,'pan',1,All_data,'vessel','Ntfy_PAN_No.',l,'[a-z0-9]{10}',0)
        if All_data['Ntfy_PAN_No.']==0:
            data_extractor_alphanumeric(text_alll,'pan',1,All_data,'\n','Ntfy_PAN_No.',l,'[a-z0-9]{10}',0)


        ##NOTIFY GST NO

        data_extractor_alphanumeric(text_alll,'gst number',1,All_data,'notify','Ntfy_GST_No.',l,'\d+\w+',0)
        if All_data['Ntfy_GST_No.']==0:
            data_extractor_alphanumeric(text_alll,'gst',1,All_data,'.com','Ntfy_GST_No.',l,'\d+\w+',0)
        if All_data['Ntfy_GST_No.']==0:
            data_extractor_alphanumeric(text_alll,'gstn',1,All_data,'\n','Ntfy_GST_No.',l,'\d+\w+',0)


        ##PORT OF LOADING

        data_extractor_alphanumeric(text_alll,'port of discharge',1,All_data,'of packages','Port_of_Loading',l,'montreal|charleston',0)
        if All_data['Port_of_Loading']==0:
            data_extractor_alphanumeric(text_alll,'port of loading',1,All_data,'port of discharge','Port_of_Loading',l,'qingdao\,china|shanghai\,china|shekou\,\schina|rotterdam|genoa',0)


        ##PORT OF DISCHARGE

        data_extractor_alphanumeric(text_alll,'port of discharge',1,All_data,'of packages','Port_of_Discharge',l,'mundra|jawaharlal\snehru',0)
        if All_data['Port_of_Discharge']==0:
            data_extractor_alphanumeric(text_alll,'port of discharge',1,All_data,'marks','Port_of_Discharge',l,'nhava\ssheva\,india|chennai\,\sindia|nhava\ssheva\sjnpt|nhava\ssheva',0)
        if All_data['Port_of_Discharge']==0:
            data_extractor_alphanumeric(text_alll,'final destination',1,All_data,'container no.','Port_of_Discharge',l,'nhava\ssheva\,\sindia',0)


        ##PLACE OF DELIVERY

        data_extractor_alphanumeric(text_alll,'place of delivery',1,All_data,'marks','Place of Delivery',l,'nhava\ssheva\,india|chennai\,\sindia|nhava\ssheva',1)
        if All_data['Place of Delivery']==0:
            data_extractor_alphanumeric(text_alll,'final destination',1,All_data,'container no.','Place of Delivery',l,'nhava\ssheva\,\sindia',1)


        ##VESSEL NAME

        data_extractor_alphanumeric(text_alll,'transport b/l.',1,All_data,'port of loading','Vessel_Name',l,'[a-z]+\s[a-z\s]+',1)
        if All_data['Vessel_Name']==0:
            data_extractor_alphanumeric(text_alll,'form no.',1,All_data,'port of discharge','Vessel_Name',l,'[a-z]+\s[a-z\s]+',0)
        if All_data['Vessel_Name']==0:
            data_extractor_alphanumeric(text_alll,'pre-carriage by',1,All_data,'port of loading','Vessel_Name',l,'cosco\sthailand',0)
        if All_data['Vessel_Name']==0:
            data_extractor_alphanumeric(text_alll,'port of loading',1,All_data,'india','Vessel_Name',l,'maersk\sguayaquil\s[\(0-9e\)]+',0)
        if All_data['Vessel_Name']==0:
            data_extractor_alphanumeric(text_alll,'port of loading',1,All_data,'fax','Vessel_Name',l,'[a-z]+\s[a-z]+\s[a-z]+\s[a-z]+\s\d\w+',0)


        ##VOYAGE NO

        data_extractor_alphanumeric(text_alll,'transport b/l.',1,All_data,'port of loading','Voyage_No',l,'\d{3}\w',0)
        if All_data['Voyage_No']==0:
            data_extractor_alphanumeric(text_alll,'form no.',1,All_data,'port of discharge','Voyage_No',l,'[a-z0-9]{9}|\d{3}\w',0)
        if All_data['Voyage_No']==0:
            data_extractor_alphanumeric(text_alll,'pre-carriage by',1,All_data,'port of receipt','Voyage_No',l,'\d{3}\w',0)


        ##CONTAINER NO

        data_extractor_alphanumeric(text_alll,'elivery)',1,All_data,'shipper seal','Container_No',l,'\w{4}\d{7}',0)
        if All_data['Container_No']==0:
            data_extractor_alphanumeric(text_alll,'container / seal no.',2,All_data,'/fcl/fcl','Container_No',l,'\w{4}\d{7}',0)
        if All_data['Container_No']==0:
            data_extractor_alphanumeric(text_alll,'container / seal no.',1,All_data,'/fcl/fcl','Container_No',l,'\w{4}\d{7}',0)
        if All_data['Container_No']==0:
            data_extractor_alphanumeric(text_alll,'measurement',1,All_data,'packages','Container_No',l,'\w{4}\d{7}',0)
        if All_data['Container_No']==0:
            data_extractor_alphanumeric(text_alll,'container :',1,All_data,'seal','Container_No',l,'\w{4}\s[0-9\-]+',0)


        ##CONTAINER GROSS WEIGHT
        data_extractor_alphanumeric(text_alll,'measurement',1,All_data,'hs code','Cntr_Gross_Weight',l,'[0-9\.\,]+[0-9\s]+kgs',0)


        ##HS CODE

        data_extractor_alphanumeric(text_alll,'hs code',1,All_data,'freight','HS_CODE',l,'[0-9]{4}\.[0-9]{4}|[0-9]{8}|[0-9]{6}',0)


        ##DATE OF ISSUE
        

        data_extractor_alphanumeric(text_alll,'board date',1,All_data,'forwarder','Date_of_Issue',l,'\d+\-\d+\-\d+',0)
        if All_data['Date_of_Issue']==0:
            data_extractor_alphanumeric(text_alll,'date of issue',1,All_data,'sign','Date_of_Issue',l,'\d+\-\w+\-\d{4}|\d+\s\w+\s\d{4}|\d{4}\-\w+\-\d+',0)

        place=data_extractor_alphanumeric(text_alll,'place of receipt',1,All_data,'ocean vessel','Place_of_receipt',l,'\D+',0).strip()
        All_data['Place_of_receipt']=place
        if All_data['Place_of_receipt']=='Keyword Not Found':
            place=data_extractor_alphanumeric(text_alll,'place of receipt',1,All_data,'port of loading','Place_of_receipt',l,'[a-z]+',-1).strip()
        

##        data_extractor_alphanumeric(text_alll,'port of discharge',1,All_data,'marks','port_of_discharge',l,'[\w]+\s[\w]+\,\w+',0)
##        data_extractor_alphanumeric(text_alll,'seal no. or packages',1,All_data,'-','port_of_discharge',l,'','')
        
        #BL GROSS WEIGHT & UQM
        data_extractor_alphanumeric(text_alll,'gross weight measurement',1,All_data,'cbm','gross_weight',l,'[0-9\.\,]+',-2)
        if All_data['gross_weight']==0:
            
            data_extractor_alphanumeric(text_alll,'weight measurement',1,All_data,'cbm','gross_weight',l,'[0-9\.\,]+',-2)
        if All_data['gross_weight']==0:
            data_extractor_alphanumeric(text_alll,'gross weight',1,All_data,'kgs','gross_weight',l,'[0-9\.\,]+',-1)
            
        #BL GROSS WEIGHT  UQM
        data_extractor_alphanumeric(text_alll,'gross weight measurement',1,All_data,'cbm','BL_WEIGHT_UQM',l,'[a-zA-Z]+',-1)
        if All_data['BL_WEIGHT_UQM']=='Found':
            data_extractor_alphanumeric(text_alll,'weight measurement',1,All_data,'cbm','BL_WEIGHT_UQM',l,'[a-zA-Z]+',-1)
        if All_data['BL_WEIGHT_UQM']=='Found':
            data_extractor_alphanumeric(text_alll,'gross weight',1,All_data,'cbm','BL_WEIGHT_UQM',l,'kgs',-1)
        
                    

        #MEASUREMENT & UQM
        data_extractor_alphanumeric(text_alll,'gross weight measurement',1,All_data,'cbm','MEASUREMENT',l,'[0-9\.\,]+',-1)
        if All_data['MEASUREMENT']==0:
            data_extractor_alphanumeric(text_alll,'weight measurement',1,All_data,'cbm','MEASUREMENT',l,'[0-9\.\,]+',-1)#cbm cft mq m^3

        if All_data['MEASUREMENT']==0:
            data_extractor_alphanumeric(text_alll,'gross weight',1,All_data,'cbm','MEASUREMENT',l,'[0-9\.\,]+',-1)#
        #MEASUREMENT UQM
        data_extractor_alphanumeric(text_alll,'gross weight measurement',1,All_data,'hose size','MEASUREMENT_UQM',l,'[a-zA-Z\^]+',-1)
        if All_data['MEASUREMENT_UQM']=='Found':
            data_extractor_alphanumeric(text_alll,'weight measurement',1,All_data,'size','MEASUREMENT_UQM',l,'cbm|cft|mq|m^3',-1)
        if All_data['MEASUREMENT_UQM']==0:
            data_extractor_alphanumeric(text_alll,'weight measurement',1,All_data,'container','MEASUREMENT_UQM',l,'cbm|cft|mq|m^3',-1)

        if All_data['MEASUREMENT_UQM']==0:
            data_extractor_alphanumeric(text_alll,'weight measurement',1,All_data,'hs','MEASUREMENT_UQM',l,'cbm|cft|mq|m^3',-1)

        if All_data['MEASUREMENT_UQM']==0:
            data_extractor_alphanumeric(text_alll,'gross weight',1,All_data,'hs','MEASUREMENT_UQM',l,'cbm|cft|mq|m^3',-1)

##        if All_data['MEASUREMENT_UQM']==0:
##            data_extractor_alphanumeric(text_alll,'weight measurement',1,All_data,'hs','MEASUREMENT_UQM',l,'cbm|cft|mq|m^3',-1)

        #shipper_seal_2
        data_extractor_alphanumeric(text_alll,'container',2,All_data,'seal','Shipper_seal_2',l,'\w+\s\d+\-\d',0) #7
        if All_data['Shipper_seal_2']==0:
            data_extractor_alphanumeric(text_alll,'place',3,All_data,'packages','Shipper_seal_2',l,'[a-z]+\d+',0) #1
        if All_data['Shipper_seal_2']==0:
            data_extractor_alphanumeric(text_alll,'seal',2,All_data,'lots','Shipper_seal_2',l,'\w+',1)  #2
        if All_data['Shipper_seal_2']=='Not':
            data_extractor_alphanumeric(text_alll,'term',1,All_data,'cases','Shipper_seal_2',l,'[a-z]+\d+',0) #4
        if All_data['Shipper_seal_2']==0:
            data_extractor_alphanumeric(text_alll,'measurement',1,All_data,'packages','Shipper_seal_2',l,'\w+',0) #5
        if All_data['Shipper_seal_2']=='pratish':
            data_extractor_alphanumeric(text_alll,'container',1,All_data,'seal','Shipper_seal_2',l,'\w+\s\w+\-\d',0) # 6
        #if All_data['Shipper_seal_2']==0:
        #data_extractor_alphanumeric(text_alll,'container',2,All_data,'seal','Shipper_seal_2',l,'\w+\s\d+\-\d',0) #7

##        #description of gooods
        data_extractor_alphanumeric(text_alll,'cbm',1,All_data,'code','description_of_gooods',l,'\d\s\w+\s[a-z]+\s\w+\s\w+\s\d+\s\w+\v\w+\s\w+\s\w+\s\w+\s\w+\s\w+\s\w+\s\w+\s\w+\s\w+',0)

        #Container_Size
        data_extractor_alphanumeric(text_alll,'uacu',1,All_data,'seal','Container_Size',l,'\d{2}',3)   #7
        if All_data['Container_Size']==0:
            data_extractor_alphanumeric(text_alll,'detention',1,All_data,'packages','Container_Size',l,'\d{2}',3)  #1
        if All_data['Container_Size']==0:
            data_extractor_alphanumeric(text_alll,'shipper',4,All_data,'lots','Container_Size',l,'\d{2}',5) #2
        if All_data['Container_Size']==0:
            data_extractor_alphanumeric(text_alll,'cases',3,All_data,'declared','Container_Size',l,'\d{2}',0) #4
        if All_data['Container_Size']==0:    
            data_extractor_alphanumeric(text_alll,'measurement',1,All_data,'packages','Container_Size',l,'\d{2}',3) #5
        if All_data['Container_Size']==0:
            data_extractor_alphanumeric(text_alll,'container',1,All_data,'seal','Container_Size',l,'\d{2}',3) #   6
        #data_extractor_alphanumeric(text_alll,'uacu',1,All_data,'seal','Container_Size',l,'\d{2}',3)   #7


        #container_type
        data_extractor_alphanumeric(text_alll,'uacu',1,All_data,'seal','container_type',l,'[a-z]{2,3}',0)  #7
        if All_data['container_type']=='eyw':
            data_extractor_alphanumeric(text_alll,'place',3,All_data,'packages','container_type',l,'[a-z]{2,3}',5)  #1
        if All_data['container_type']==0:
            data_extractor_alphanumeric(text_alll,'seal',2,All_data,'lots','container_type',l,'[a-z]{2,3}',1)   #2
        if All_data['container_type']=='al':
            data_extractor_alphanumeric(text_alll,'measurement',1,All_data,'packages','container_type',l,'[a-z]{2,3}',1)   #5
        if All_data['container_type']=='ord':
            data_extractor_alphanumeric(text_alll,'hasu',1,All_data,'seal','container_type',l,'[a-z]{2,3}',0)   #6
        #data_extractor_alphanumeric(text_alll,'uacu',1,All_data,'seal','container_type',l,'[a-z]{2,3}',0)  #7
        #data_extractor_alphanumeric(text_alll,'measurement',1,All_data,'packages','container_type',l,'[a-z]{2,3}',1) #4


##        #Container_Pkgs
##
##        data_extractor_alphanumeric(text_alll,'contain',3,All_data,'plastic','Container_Pkgs',l,'\d+6',0)
        

        #Container_Gross Wt
        data_extractor_alphanumeric(text_alll,'pallet',1,All_data,'cbm','Container_Gross Wt',l,'\d+\,\d+',0)         # 7
        if All_data['Container_Gross Wt']==0:
            data_extractor_alphanumeric(text_alll,'packages',1,All_data,'to','Container_Gross Wt',l,'\d+\.\d+',0) #1
        if All_data['Container_Gross Wt']==0:
            data_extractor_alphanumeric(text_alll,'charleston',2,All_data,'cbm','Container_Gross Wt',l,'\d+\.\d+',0) #2
        if All_data['Container_Gross Wt']==0:
            data_extractor_alphanumeric(text_alll,'total',1,All_data,'cbm','Container_Gross Wt',l,'\d+\.\d+',0) #4
        if All_data['Container_Gross Wt']=='13.150':
            data_extractor_alphanumeric(text_alll,'seal',2,All_data,'in','Container_Gross Wt',l,'\d+\.\d+',0) #5
        if All_data['Container_Gross Wt']==0:
            data_extractor_alphanumeric(text_alll,'stc',1,All_data,'packaging','Container_Gross Wt',l,'\d+\,\d+',0) #6
        #data_extractor_alphanumeric(text_alll,'pallet',1,All_data,'cbm','Container_Gross Wt',l,'\d+\,\d+',0)         # 7

        
        now = datetime.now()
        current_tim = now.strftime("%H:%M:%S")
        All_data['End_Time']=current_tim

        print(All_data['Cntr_Gross_Weight'])
        print(All_data)
##            All_data['File_Name']=file
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        All_data['Start_Time']=current_time

##        query="insert into BL_OCR values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
##        values=(All_data['BL_No'],All_data['BL_Date'],All_data['Shipper'],All_data['Shipper_Country'],All_data['Consignee'],All_data['Consignee_Address_1'],All_data['Consignee_Address_2'],All_data['Consignee_Address_3'],All_data['Consignee_Country'],All_data['Cnee_IEC_No'],All_data['Cnee_PAN_No.'],All_data['Cnee_GST_No.'],All_data['Cnee_Email_Id'],All_data['Notify_Party'],All_data['Notify_Party_Address_1'],All_data['Notify_Party_Address_2'],All_data['Notify_Party_Address_3'],All_data['Notify_Country'],All_data['Ntfy_PAN_No.'],All_data['Ntfy_GST_No.'],All_data['Port_of_Loading'],All_data['Place of Delivery'],All_data['Vessel_Name'],All_data['Voyage_No'],All_data['Container_No'],All_data['Cntr_Gross_Weight'],All_data['HS_CODE'],All_data['Date_of_Issue'],All_data['Place_of_receipt'],All_data['gross_weight'],All_data['BL_WEIGHT_UQM'],All_data['MEASUREMENT'],All_data['MEASUREMENT_UQM'],All_data['shipper_seal_2'],All_data['Container_Size'],All_data['container_type'],All_data['Container_Gross Wt'])
##        cursor.execute(query,values)   
##        conn.commit()
    print('===================== Next PDF ========================')

##print(BL_Extraction(r"C:\Users\vaio\Downloads\BL\BL\allpdf\new\ECU_MILNAV23064.pdf",r"C:\Users\vaio\Downloads\BL\BL\allpdf\new"))
####
for file in os.listdir(r"D:\extract_pdf"):
    file2=(r"D:\extract_pdf\%s")%file
##    file = file.lower()
    print(file)
    if file.endswith('.pdf'):
        print(BL_Extraction(file2,file))
##        
