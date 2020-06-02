import pyexcel
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Font, Fill
from .objectcollection import ObjectCollection

class Output(object):
    
    def __init__(self):
        
        return

    
    def Print_Mass(self, material_streams, work_book):
        
        sheet = 'Mass balances v2' 
        
        
        wb = load_workbook(work_book)
    
        # if the sheet doesn't exist, create a new sheet
        try:
            sheet = wb[sheet]
        except:
            sheet = wb.create_sheet(sheet)

        count = 0
        feed_count, feed_mass = 0, 0
        product_count,product_mass = 0, 0
        waste_count, waste_mass = 0, 0


        rw = 19

        for name, obj in material_streams.items():
            comp_count = 0

            if obj.type == 'Feed':
                row_start = rw + count
                for comp, frac in obj.massfrac.items():
                
                    if frac >= 0.0001:
                        
                        sheet.cell(row=row_start + comp_count , column=4).value = comp
                        sheet.cell(row=row_start + comp_count , column=5).value = frac * 100
                        comp_count += 1
                        count += 1
                        feed_count += 1

                sheet.merge_cells(start_row= row_start, start_column=2, end_row=row_start+comp_count-1, end_column=2)
                sheet.cell(row= row_start , column=2).value = name
                sheet.merge_cells(start_row= row_start, start_column=3, end_row=row_start+comp_count-1, end_column=3)
                massflow = obj.massflow * 8000 / 1000 / 1000
                feed_mass += massflow
                sheet.cell(row= row_start , column=3).value = massflow
                sheet.merge_cells(start_row= row_start, start_column=6, end_row=row_start+comp_count-1, end_column=6)
                sheet.cell(row= row_start , column=6).value = obj.temperature
                sheet.merge_cells(start_row= row_start, start_column=7, end_row=row_start+comp_count-1, end_column=7)
                sheet.cell(row= row_start , column=7).value = obj.pressure


            if obj.type == 'Product':
                row_start = rw + count + 3
                for comp, frac in obj.massfrac.items():
                    if frac >= 0.0001:

                        sheet.cell(row=row_start + comp_count , column=4).value = comp
                        sheet.cell(row=row_start + comp_count , column=5).value = frac * 100
                        comp_count += 1
                        count += 1
                        product_count += 1

                sheet.merge_cells(start_row= row_start, start_column=2, end_row=row_start+comp_count-1, end_column=2)
                sheet.cell(row= row_start , column=2).value = name
                sheet.merge_cells(start_row= row_start, start_column=3, end_row=row_start+comp_count-1, end_column=3)
                massflow = obj.massflow * 8000 / 1000 / 1000
                product_mass += massflow
                sheet.cell(row= row_start , column=3).value = massflow
                sheet.merge_cells(start_row= row_start, start_column=6, end_row=row_start+comp_count-1, end_column=6)
                sheet.cell(row= row_start , column=6).value = obj.temperature
                sheet.merge_cells(start_row= row_start, start_column=7, end_row=row_start+comp_count-1, end_column=7)
                sheet.cell(row= row_start , column=7).value = obj.pressure


            if obj.type == 'Waste':
                row_start = rw + count + 6
                for comp, frac in obj.massfrac.items():
                    if frac >= 0.0001:
                        sheet.cell(row=row_start + comp_count , column=4).value = comp
                        sheet.cell(row=row_start + comp_count , column=5).value = frac * 100
                        comp_count += 1
                        waste_count += 1
                        count += 1

                sheet.merge_cells(start_row= row_start, start_column=2, end_row=row_start+comp_count-1, end_column=2)
                sheet.cell(row= row_start , column=2).value = name
                sheet.merge_cells(start_row= row_start, start_column=3, end_row=row_start+comp_count-1, end_column=3)
                massflow = obj.massflow * 8000 / 1000 / 1000
                waste_mass += massflow
                sheet.cell(row= row_start , column=3).value = massflow
                sheet.merge_cells(start_row= row_start, start_column=6, end_row=row_start+comp_count-1, end_column=6)
                sheet.cell(row= row_start , column=6).value = obj.temperature
                sheet.merge_cells(start_row= row_start, start_column=7, end_row=row_start+comp_count-1, end_column=7)
                sheet.cell(row= row_start , column=7).value = obj.pressure
        
        # Print feed headers
        feed_start = rw
        c = sheet.cell(row= feed_start-3 , column=2)
        c.value = 'Mass balances'
        c.font = Font(bold=True)
        c = sheet.cell(row= feed_start-2 , column=2)
        c.value = 'Raw materials' 
        c.font = Font(bold=True)
        c = sheet.cell(row= feed_start-1 , column=2)
        c.value = 'Stream' 
        c.font = Font(bold=True)
        c = sheet.cell(row= feed_start-1 , column=3)
        c.value = 'Flowrate ktonne/y'
        c.font = Font(bold=True)
        c = sheet.cell(row= feed_start-1 , column=4)
        c.value = 'Concentration (wt%)'
        c.font = Font(bold=True)
        c = sheet.cell(row= feed_start-1 , column=6)
        c.value = 'Temperature ( C )'
        c.font = Font(bold=True)
        c = sheet.cell(row= feed_start-1 , column=7)
        c.value = 'Pressure (bar)'
        c.font = Font(bold=True)

        # Print product headers 
        prod_start = feed_start + feed_count + 3
        c = sheet.cell(row= prod_start-2 , column=2)
        c.value = 'Products'
        c.font = Font(bold=True)
        c = sheet.cell(row= prod_start-1 , column=2)
        c.value = 'Stream'
        c.font = Font(bold=True)
        c = sheet.cell(row= prod_start-1 , column=3)
        c.value = 'Flowrate ktonne/y'
        c.font = Font(bold=True)
        c = sheet.cell(row= prod_start-1 , column=4)
        c.value = 'Concentration (wt%)'
        c.font = Font(bold=True)
        c = sheet.cell(row= prod_start-1 , column=6)
        c.value = 'Temperature ( C )'
        c.font = Font(bold=True)
        c = sheet.cell(row= prod_start-1 , column=7)
        c.value = 'Pressure (bar)'
        c.font = Font(bold=True)

        # Print waste headers
        wast_start = prod_start + product_count + 3
        c = sheet.cell(row= wast_start-2 , column=2)
        c.value = 'Waste streams'
        c.font = Font(bold=True)
        c = sheet.cell(row= wast_start-1 , column=2)
        c.value = 'Stream'
        c.font = Font(bold=True)
        c = sheet.cell(row= wast_start-1 , column=3)
        c.value = 'Flowrate ktonne/y'
        c.font = Font(bold=True)
        c = sheet.cell(row= wast_start-1 , column=4)
        c.value = 'Concentration (wt%)'
        c.font = Font(bold=True)
        c = sheet.cell(row= wast_start-1 , column=6)
        c.value = 'Temperature ( C )'
        c.font = Font(bold=True)
        c = sheet.cell(row= wast_start-1 , column=7)
        c.value = 'Pressure (bar)'
        c.font = Font(bold=True)


        # Print Balance check
        check_start = wast_start + waste_count
        c = sheet.cell(row=check_start-6, column= 9)
        c.value = 'Balance check'
        c.font = Font(bold=True)
        c = sheet.cell(row=check_start-5, column= 9)
        c.value = 'Total inputs'
        c.font = Font(bold=True)
        c = sheet.cell(row=check_start-5, column= 10)
        c.value = 'Total F.rate ktonne/y '
        c.font = Font(bold=True)
        c = sheet.cell(row=check_start-4, column= 9)
        c.value = 'Raw materials'
        c.font = Font(bold=True)
        sheet.cell(row=check_start-4, column= 10).value = feed_mass
        c = sheet.cell(row=check_start-3, column= 9)
        c.value = 'Products'
        c.font = Font(bold=True)
        sheet.cell(row=check_start-3, column= 10).value = product_mass
        c = sheet.cell(row=check_start-2, column= 9)
        c.value = 'Waste streams'
        c.font = Font(bold=True)
        sheet.cell(row=check_start-2, column= 10).value = waste_mass
        c = sheet.cell(row=check_start-1, column= 9)
        c.value = 'Balance check'
        c.font = Font(bold=True)
        sheet.cell(row=check_start-1, column= 10).value = feed_mass - product_mass - waste_mass
        c = sheet.cell(row=check_start-0, column= 9)
        c.value = 'Balance error'
        c.font = Font(bold=True)
        sheet.cell(row=check_start-0, column= 10).value = (feed_mass - product_mass - waste_mass)/feed_mass*100


        wb.save(work_book)


    def Print_Energy(self, utilities, work_book):
        
        sheet = 'Energy balances v2' 
        
        wb = load_workbook(work_book)
        try:
            sheet = wb[sheet]
        except:
            wb.create_sheet(sheet)

        count_right = 0
        count_left = 0
        count_lps, count_mps, count_hps, count_frig = 0, 0, 0, 0
        count_elec, count_natgas, count_cw = 0, 0, 0
        rw = 29
        
        for util, block1 in utilities.items():
            for block2, data in block1.items():

                if (util == 'LPS' or util == 'LPS-GEN'):
                    cur_row = rw + count_left
                    ii = 0
                    count_left += 1
                    count_lps += 1
                elif (util == 'MPS' or util == 'MPS-GEN'):
                    cur_row = rw + count_left + 3
                    ii = 0
                    count_left += 1
                    count_mps += 1
                elif (util == 'HPS' or util == 'HPS-GEN'):
                    cur_row = rw + count_left + 6
                    ii = 0
                    count_left += 1
                    count_hps += 1
                elif util == 'RF':
                    cur_row = rw + count_left + 9
                    ii = 0
                    count_left += 1
                    count_frig += 1
                elif util == 'ELECTRIC':
                    cur_row = rw + count_right
                    ii = 8
                    count_right += 1
                    count_elec += 1
                elif util == 'NATGAS':
                    cur_row = rw + count_right + 3
                    ii = 8
                    count_right += 1
                    count_natgas += 1
                elif util == 'CW':
                    cur_row = rw + count_right + 6
                    ii = 8
                    count_right += 1
                    count_cw += 1
            
                if util == 'ELECTRIC':
                    sheet.cell(row=cur_row, column=2+ii).value = block2
                    sheet.cell(row=cur_row, column=4+ii).value = data.duty * 4186.8
                elif util =='NATGAS':
                    sheet.cell(row=cur_row, column=2+ii).value = block2
                    sheet.cell(row=cur_row, column=6+ii).value = data.usage * 8000 / 1000 / 1000

                else:
                    if '-GEN' in util:
                        sheet.cell(row=cur_row, column=2+ii).value = block2
                        sheet.cell(row=cur_row, column=4+ii).value = -data.duty * 4186.8
                        sheet.cell(row=cur_row, column=5+ii).value = -data.duty * 4186.8 * 8000 * 1E-6
                        sheet.cell(row=cur_row, column=6+ii).value = -data.usage * 8000 / 1000 / 1000
                    else:
                        sheet.cell(row=cur_row, column=2+ii).value = block2
                        sheet.cell(row=cur_row, column=4+ii).value = data.duty * 4186.8
                        sheet.cell(row=cur_row, column=5+ii).value = data.duty * 4186.8 * 8000 * 1E-6
                        sheet.cell(row=cur_row, column=6+ii).value = data.usage * 8000 / 1000 / 1000
    
        headers = ['Unit name','Unit description','Duty -MJ/hr', 'Duty -TJ/y', 'Mass -ktonne/y', 'Remark']
        headelec = ['Unit name','Unit description','Power -kW', 'Energy -GWh/y', 'Energy - TJ/y', 'Remark']
        # Print low pressure steam header
        count_col = 2
        lowpres_start = rw
        c =  c = sheet.cell(row=lowpres_start-3 , column=count_col)
        c.value = 'Breakdown of requirements'
        c.font = Font(bold=True)
        c = sheet.cell(row=lowpres_start-2 , column=count_col)
        c.value = 'Low pressure steam'
        c.font = Font(bold=True)
        for head in headers:
            c = sheet.cell(row=lowpres_start-1 , column=count_col)
            c.value = head
            c.font = Font(bold=True)
            count_col += 1
        # Print medium pressure steam header
        mp_start = lowpres_start + count_lps + 3
        count_col = 2
        c = sheet.cell(row=mp_start-2 , column=count_col)
        c.value = 'Medium pressure steam'
        c.font = Font(bold=True)
        for head in headers:
            c = sheet.cell(row=mp_start-1 , column=count_col)
            c.value = head
            c.font = Font(bold=True)
            count_col += 1
        # Print high pressure steam header
        hp_start = mp_start + count_mps + 3 
        count_col = 2
        c = sheet.cell(row=hp_start-2 , column=count_col)
        c.value = 'High pressure steam'
        c.font = Font(bold=True)
        for head in headers:
            c = sheet.cell(row=hp_start-1 , column=count_col)
            c.value = head
            c.font = Font(bold=True)
            count_col += 1
        # Print refrigerator header
        frig_start = hp_start + count_hps + 3
        count_col = 2
        c = sheet.cell(row=frig_start-2 , column=count_col)
        c.value = 'Refrigerator'
        c.font = Font(bold=True)
        for head in headers:
            c = sheet.cell(row=frig_start-1 , column=count_col)
            c.value = head
            c.font = Font(bold=True)
            count_col += 1
        # Print electricity header
        elec_start = rw
        count_col = 10
        c = sheet.cell(row=elec_start-2 , column=count_col)
        c.value = 'Electricity'
        c.font = Font(bold=True)
        for head in headelec:
            c = sheet.cell(row=elec_start-1 , column=count_col)
            c.value = head
            c.font = Font(bold=True)
            count_col += 1
        # Print natural gas header
        natgas_start = elec_start+ count_elec + 3
        count_col = 10
        c = sheet.cell(row=natgas_start-2 , column=count_col)
        c.value = 'Natural gas'
        c.font = Font(bold=True)
        for head in headers:
            c = sheet.cell(row=natgas_start-1 , column=count_col)
            c.value = head
            c.font = Font(bold=True)
            count_col += 1
        # Print cool water header
        water_start = natgas_start + count_natgas + 3
        count_col = 10
        c = sheet.cell(row=water_start-2 , column=count_col)
        c.value = 'Cooling water'
        c.font = Font(bold=True)
        for head in headers:
            c = sheet.cell(row=water_start-1 , column=count_col)
            c.value = head
            c.font = Font(bold=True)
            count_col += 1

        wb.save(work_book)