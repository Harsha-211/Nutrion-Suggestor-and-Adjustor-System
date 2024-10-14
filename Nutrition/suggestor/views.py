from django.shortcuts import render
from django.http import HttpResponse

from Nutrition.settings import GOOGLE_API_KEY
from .forms import MealForm
from .models import FoodItem
import google.generativeai as genai
from django.utils.safestring import mark_safe


MaxCarbs = 0
MaxPro = 0
MaxFat = 0
MaxCal = 0
MaxFib = 0
MinCarbs = 0
MinPro = 0
MinFat = 0
MinCal = 0
MinFib = 0

def adjustion(diet, age , weight , activity , gender):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(str(diet)+", adjust this diet plan based on my weight"+str(weight)+", Age "+str(age)+", Gender "+str(gender)+" and activity status "+str(activity)+". donot remove any food item just adjust them . The given diet belongs to a region only add that region id adding is needed . Only give output in format Current diet , break fast: , lunch: , dinner: ,snack: , Adjusted diet break fast: , lunch: , dinner: ,snack: , General considerations . Add any food item if required that belongs to same region and donot add any extra lines than that required for mentioned format .Add 'br'tag at every end of a sentence and use 'h2' tag for headings instead of '**'")
    return response

def BMR(age , weight , gender):
    if gender.lower() == "male":
        if(age<3):
            return (59.512*weight-30.4+70 , 59.512*weight-30.4-70)
        elif(age>=3 and age<10):
            return (22.706*weight+504.3+67 , 22.706*weight+504.3-67)
        elif (age>=10 and age<18):
            return (17.686*weight+658.2+105 , 17.686*weight+658.2-105)
        elif(age>=18 and age<30):
            return (15.057*weight+692.2+153 , 15.057*weight+692.2-153)
        elif(age>=30 and age<60):
            return (11.472*weight+873.1+167 , 11.472*weight+873.1-167)
        else:
            return (11.711*weight+587.7+164 , 11.711*weight+587.7-164) 
    else:
        if(age<3):
            return (58.317*weight-31.1+59 , 58.317*weight-31.1-59)
        elif(age>=3 and age<10):
            return (20.315*weight+485.9+70 , 20.315*weight+485.9-70)
        elif (age>=10 and age<18):
            return (13.384*weight+692.6+111 , 13.384*weight+692.6-111)
        elif(age>=18 and age<30):
            return (14.818*weight+486.6+119 , 14.818*weight+486.6-119)
        elif(age>=30 and age<60):
            return (8.126*weight+845.6+111 , 8.126*weight+845.6-111)
        else:
            return (9.082*weight+658.5+108 , 9.082*weight+658.5-108)

def  ActivityConst(activity,gender):
    if(activity.lower() == 'sedentary'):
        return 1.3
    elif(activity.lower() == 'lightly active'):
        if(gender.lower() == 'male'):
            return 1.6
        else:
            return 1.5
    elif(activity.lower() == "moderate activity"):
        if(gender.lower() == "male"):
            return 1.7
        else:
            return 1.6
    elif(activity.lower() == "very active"):
        if(gender.lower() == "male"):
            return 2.1
        else:
            return 1.9
    else:
        if(gender.lower()=='male'):
            return 2.4
        else:
            return 2.2   
        
def nutrition_analysis(request):
    item_names = FoodItem.objects.all()
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            breakfast = form.cleaned_data['breakfast']
            brquantity = form.cleaned_data['brquantity']
            lunch = form.cleaned_data['lunch']
            lquantity = form.cleaned_data['lquantity']
            dinner = form.cleaned_data['dinner']
            dquantity = form.cleaned_data['dquantity']
            snacks = form.cleaned_data['snacks']
            squantity = form.cleaned_data['squantity']
            age = form.cleaned_data['age']
            weigth = form.cleaned_data['weigth']
            gender = form.cleaned_data['gender']
            activity = form.cleaned_data['activity']
            
            breakfast_items = list(breakfast.split(','))
            breakfast_items = [items.strip() for items in breakfast_items]
            
            breakfast_quantity = list(brquantity.split(','))
            breakfast_quantity = [items.strip() for items in breakfast_quantity]
            
            breakfast_string = "Breakfast:"+','.join(f"{q}{bf}" for q,bf in zip(breakfast_quantity , breakfast_items))
            
            lunch_items = list(lunch.split(','))
            lunch_items = [items.strip() for items in lunch_items]
            
            lunch_quantity = list(lquantity.split(','))
            lunch_quantity = [items.strip() for items in lunch_quantity]
            
            lunch_string = " Lunch:"+','.join(f"{q}{l}" for q,l in zip(lunch_quantity , lunch_items))
            
            dinner_items = list(dinner.split(','))
            dinner_items = [items.strip() for items in dinner_items]
            
            dinner_quantity = list(dquantity.split(','))
            dinner_quantity = [items.strip() for items in dinner_quantity]
            
            dinner_string = " Dinner:"+','.join(f"{q}{d}" for q,d in zip(dinner_quantity , dinner_items))
            
            snack_items = list(snacks.split(','))
            snack_items = [items.strip() for items in snack_items]
            
            snack_quantity = list(squantity.split(','))
            snack_quantity = [items.strip() for items in snack_quantity]
            
            snack_string = ' Snacks:'+','.join(f"{q}{s}" for q,s in zip(snack_quantity , snack_items))
            
            Diet = breakfast_string+lunch_string+dinner_string+snack_string
            #BreakFast 
            BcurrCarbs, BcurrPro, BcurrFat, BcurrCal = 0, 0, 0, 0
            breakfast_quantities = list(map(int, breakfast_quantity))  # Convert to integers

            for i in range(len(breakfast_items)):
                food_item = breakfast_items[i]
                quantity = breakfast_quantities[i]

                food_items = FoodItem.objects.filter(name__iexact=food_item)

                if food_items.exists():
                    food = food_items.first()
                    BcurrCarbs += food.carbohydrates * quantity
                    BcurrPro += food.proteins * quantity
                    BcurrFat += food.fats * quantity
                    BcurrCal += food.calories * quantity
                else:
                    print(f"Food item '{food_item}' not found in the database.")

            # Lunch Nutrient Calculation
            LcurrCarbs, LcurrPro, LcurrFat, LcurrCal = 0, 0, 0, 0
            lunch_quantities = list(map(int, lunch_quantity))  # Convert to integers

            for i in range(len(lunch_items)):
                food_item = lunch_items[i]
                quantity = lunch_quantities[i]

                food_items = FoodItem.objects.filter(name__iexact=food_item)

                if food_items.exists():
                    food = food_items.first()
                    LcurrCarbs += food.carbohydrates * quantity
                    LcurrPro += food.proteins * quantity
                    LcurrFat += food.fats * quantity
                    LcurrCal += food.calories * quantity
                else:
                    print(f"Food item '{food_item}' not found in the database.")

            # Dinner Nutrient Calculation
            DcurrCarbs, DcurrPro, DcurrFat, DcurrCal = 0, 0, 0, 0
            dinner_quantities = list(map(int, dinner_quantity))  # Convert to integers

            for i in range(len(dinner_items)):
                food_item = dinner_items[i]
                quantity = dinner_quantities[i]

                food_items = FoodItem.objects.filter(name__iexact=food_item)

                if food_items.exists():
                    food = food_items.first()
                    DcurrCarbs += food.carbohydrates * quantity
                    DcurrPro += food.proteins * quantity
                    DcurrFat += food.fats * quantity
                    DcurrCal += food.calories * quantity
                else:
                    print(f"Food item '{food_item}' not found in the database.")

            # Snacks Nutrient Calculation
            ScurrCarbs, ScurrPro, ScurrFat, ScurrCal = 0, 0, 0, 0
            snack_quantities = list(map(int, snack_quantity))  # Convert to integers

            for i in range(len(snack_items)):
                food_item = snack_items[i]
                quantity = snack_quantities[i]

                food_items = FoodItem.objects.filter(name__iexact=food_item)

                if food_items.exists():
                    food = food_items.first()
                    ScurrCarbs += food.carbohydrates * quantity
                    ScurrPro += food.proteins * quantity
                    ScurrFat += food.fats * quantity
                    ScurrCal += food.calories * quantity
                else:
                    print(f"Food item '{food_item}' not found in the database.")
            currCarbs = BcurrCarbs+LcurrCarbs+DcurrCarbs+ScurrCarbs
            currPro = BcurrPro+LcurrPro+DcurrPro+ScurrPro
            currFat = BcurrFat + LcurrFat + DcurrFat+ScurrFat
            currCal = BcurrCal+ LcurrCal + DcurrCal+ScurrCal
            #Calculating Maximum and Minimum Nutrients
            SamMaxCal,SamMinCal = BMR(age , weigth , gender)
            #Calories
            MaxCal = SamMaxCal*ActivityConst(activity ,gender)
            MinCal = SamMinCal*ActivityConst(activity,gender)
            #Protein
            MaxPro = weigth*1.2
            MinPro = weigth*0.8
            #Fat
            MaxFat = MaxCal*0.35/9
            MinFat = MinCal*0.2/9
            #carbohydrates
            MaxCarbs = (MaxCal - MaxFat*9 - MaxPro*4)/4
            MinCarbs = (MinCal - MaxFat*9 - MaxPro*4)/4
            excessCarbs = currCarbs - MaxCarbs
            excessPro = currPro - MaxPro
            excessFats = currFat - MaxFat
            excessCal = currCal - MaxCal
            
            deficientCarbs = MinCarbs - currCarbs
            deficientPro = MinPro - currPro
            deficientFat = MinFat - currFat
            deficientCal = MinCal - currCal
            
            adj = adjustion(diet=Diet , weight=weigth , age=age , gender=gender , activity=activity).text
            adj = mark_safe(adj)
            
            return render(request, 'nutrition_results.html',{
                'form': form,
                'total_carbohydrates': currCarbs,
                'total_proteins': currPro,
                'total_fat': currFat,
                'total_calories': currCal,
                'excess_carbohydrates': excessCarbs if excessCarbs > 0 else None,
                'excess_proteins': excessPro if excessPro > 0 else None,
                'excess_fats': excessFats if excessFats > 0 else None,
                'excess_calories': excessCal if excessCal > 0 else None,
                'deficient_carbohydrates': deficientCarbs if deficientCarbs > 0 else None,
                'deficient_proteins': deficientPro if deficientPro > 0 else None,
                'deficient_fats': deficientFat if deficientFat > 0 else None,
                'deficient_calories': deficientCal if deficientCal > 0 else None,
                'Adjustements': adj,
            })
    else:
        form = MealForm()
    return render(request, 'nutrition_analysis.html',{'form':form , "item_names":item_names})   