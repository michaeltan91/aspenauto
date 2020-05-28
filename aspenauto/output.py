import pyexcel
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Font, Fill

class Output(object):
    
    def __init__(self):
        
        return

    
    def Print(self, material_streams, work_book):
        
        sheet = 'Mass balances v2' 
        
        
        wb = load_workbook(work_book)
    
        # if the sheet doesn't exist, create a new sheet
        sheet = wb[sheet]

        count = 0
        feed_count = 0
        product_count = 0

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
                sheet.cell(row= row_start , column=3).value = obj.massflow['total'] * 8000 / 1000 / 1000
                sheet.merge_cells(start_row= row_start, start_column=6, end_row=row_start+comp_count-1, end_column=6)
                sheet.cell(row= row_start , column=6).value = obj.temperature
                sheet.merge_cells(start_row= row_start, start_column=7, end_row=row_start+comp_count-1, end_column=7)
                sheet.cell(row= row_start , column=7).value = obj.pressure


            if obj.type == 'Product':
                row_start = rw + count + 4
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
                sheet.cell(row= row_start , column=3).value = obj.massflow['total'] * 8000 / 1000 / 1000
                sheet.merge_cells(start_row= row_start, start_column=6, end_row=row_start+comp_count-1, end_column=6)
                sheet.cell(row= row_start , column=6).value = obj.temperature
                sheet.merge_cells(start_row= row_start, start_column=7, end_row=row_start+comp_count-1, end_column=7)
                sheet.cell(row= row_start , column=7).value = obj.pressure


            if obj.type == 'Waste':
                row_start = rw + count + 8
                for comp, frac in obj.massfrac.items():
                    if frac >= 0.0001:
                        sheet.cell(row=row_start + comp_count , column=4).value = comp
                        sheet.cell(row=row_start + comp_count , column=5).value = frac * 100
                        comp_count += 1
                        count += 1

                sheet.merge_cells(start_row= row_start, start_column=2, end_row=row_start+comp_count-1, end_column=2)
                sheet.cell(row= row_start , column=2).value = name
                sheet.merge_cells(start_row= row_start, start_column=3, end_row=row_start+comp_count-1, end_column=3)
                sheet.cell(row= row_start , column=3).value = obj.massflow['total'] * 8000 / 1000 / 1000
                sheet.merge_cells(start_row= row_start, start_column=6, end_row=row_start+comp_count-1, end_column=6)
                sheet.cell(row= row_start , column=6).value = obj.temperature
                sheet.merge_cells(start_row= row_start, start_column=7, end_row=row_start+comp_count-1, end_column=7)
                sheet.cell(row= row_start , column=7).value = obj.pressure

        feed_start = rw
        
        c = sheet.cell(row= feed_start-3 , column=2)
        c.font = Font(bold=True)

        sheet.cell(row= feed_start-3 , column=2).value = 'Mass balances'
        sheet.cell(row= feed_start-2 , column=2).value = 'Raw materials'
        sheet.cell(row= feed_start-1 , column=2).value = 'Stream'
        sheet.cell(row= feed_start-1 , column=3).value = 'Flowrate ktonne/y'
        sheet.cell(row= feed_start-1 , column=4).value = 'Concentration (wt%)'
        sheet.cell(row= feed_start-1 , column=6).value = 'Temperature ( C )'
        sheet.cell(row= feed_start-1 , column=7).value = 'Pressure (bar)'

        prod_start = feed_start + feed_count + 4
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


        wast_start = prod_start + product_count + 4
        sheet.cell(row= wast_start-2 , column=2).value = 'Waste streams'
        sheet.cell(row= wast_start-1 , column=2).value = 'Stream'
        sheet.cell(row= wast_start-1 , column=3).value = 'Flowrate ktonne/y'
        sheet.cell(row= wast_start-1 , column=4).value = 'Concentration (wt%)'
        sheet.cell(row= wast_start-1 , column=6).value = 'Temperature ( C )'
        sheet.cell(row= wast_start-1 , column=7).value = 'Pressure (bar)'

        wb.save(work_book)
                

