from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import pandas as pd

from .models import Company, DataSource, EmissionRecord


class UploadCSVView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        return Response({
            "message": "Upload endpoint ready. Use POST request with CSV file."
        })

    def post(self, request):

        file = request.FILES.get('file')

        if not file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            # Read CSV
            df = pd.read_csv(file)

            saved_records = 0

            # Create company
            company, created = Company.objects.get_or_create(
                name="Demo Company",
                defaults={"industry": "Manufacturing"}
            )

            # Create datasource
            data_source, created = DataSource.objects.get_or_create(
                company=company,
                source_type='SAP'
            )

            # Save records
            for _, row in df.iterrows():

                EmissionRecord.objects.create(
                    company=company,
                    source=data_source,
                    scope='Scope 1',
                    category='Fuel Combustion',
                    activity_type=row['fuel_type'],
                    raw_value=float(row['quantity']),
                    normalized_value=float(row['quantity']),
                    unit=row['unit'],
                    normalized_unit=row['unit'],
                    emission_factor=2.0,
                    co2e=float(row['quantity']) * 2,
                    is_suspicious=float(row['quantity']) > 1000
                )

                saved_records += 1

            return Response({
                "message": "File uploaded and data saved successfully",
                "columns": list(df.columns),
                "total_rows": len(df),
                "saved_records": saved_records
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardView(APIView):

    def get(self, request):

        total_records = EmissionRecord.objects.count()

        total_emissions = sum(
            record.co2e for record in EmissionRecord.objects.all()
        )

        suspicious_records = EmissionRecord.objects.filter(
            is_suspicious=True
        ).count()

        return Response({
            "total_records": total_records,
            "total_emissions": total_emissions,
            "suspicious_records": suspicious_records
        })