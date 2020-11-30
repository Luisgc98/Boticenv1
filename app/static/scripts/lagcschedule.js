function remove_value(){
    document.getElementById('day').value = "";
    document.getElementById('year').value = "";
    document.getElementById('date2').value = "";
    document.getElementById('time2').value = "";
    document.getElementById('confirmation').setAttribute('class', 'hidden');
    for(var i=2; i<9; i++){
        document.getElementsByClassName('nav-link')[i].removeAttribute('style');
    }
    for(var i=9; i<21; i++){
        document.getElementsByClassName('nav-link')[i].removeAttribute('style');
    }
}

var minute = document.getElementsByName('periodicity')[0];
function periodicity(action){
    if(action == 'set'){
        minute.setAttribute('checked', 'checked');
        document.getElementById('minutes').removeAttribute('class');
    }else {
        for(var i=0; i<document.getElementsByName('periodicity').length; i++){
            var valor = document.getElementsByName('periodicity')[i];
            valor.removeAttribute('checked');
        }
    }
};
minute.addEventListener('click', function(){
    remove_value();
    document.getElementById('hours').setAttribute('class', 'hidden');
    document.getElementById('days').setAttribute('class', 'hidden');
    document.getElementById('weeks').setAttribute('class', 'hidden');
    document.getElementById('months').setAttribute('class', 'hidden');
    document.getElementById('years').setAttribute('class', 'hidden');
    document.getElementById('minutes').removeAttribute('class');

    for(var i=0; i<6; i++){
        if(i != 0){
            document.getElementsByName('periodicity')[i].removeAttribute('checked');
        }
    }
    minute.setAttribute('checked', 'checked');
    document.getElementById('at_minutes').value = "1";
    document.getElementById('day').removeAttribute('required');
    document.getElementById('year').removeAttribute('required');
});

var hours = document.getElementsByName('periodicity')[1];
hours.addEventListener('click', function(){
    remove_value();
    document.getElementById('minutes').setAttribute('class', 'hidden');
    document.getElementById('days').setAttribute('class', 'hidden');
    document.getElementById('weeks').setAttribute('class', 'hidden');
    document.getElementById('months').setAttribute('class', 'hidden');
    document.getElementById('years').setAttribute('class', 'hidden');
    document.getElementById('hours').removeAttribute('class');

    for(var i=0; i<6; i++){
        if(i != 1){
            document.getElementsByName('periodicity')[i].removeAttribute('checked');
        }
    }
    hours.setAttribute('checked', 'checked');
    document.getElementById('at_hour').value = "1";
    document.getElementById('day').removeAttribute('required');
    document.getElementById('year').removeAttribute('required');
});

var days = document.getElementsByName('periodicity')[2];
days.addEventListener('click', function(){
    remove_value();
    document.getElementById('minutes').setAttribute('class', 'hidden');
    document.getElementById('hours').setAttribute('class', 'hidden');
    document.getElementById('weeks').setAttribute('class', 'hidden');
    document.getElementById('months').setAttribute('class', 'hidden');
    document.getElementById('years').setAttribute('class', 'hidden');
    document.getElementById('days').removeAttribute('class');

    for(var i=0; i<6; i++){
        if(i != 2){
            document.getElementsByName('periodicity')[i].removeAttribute('checked');
        }
    }
    days.setAttribute('checked', 'checked');
    document.getElementById('on_day').value = "1";
    document.getElementById('day').removeAttribute('required');
    document.getElementById('year').removeAttribute('required');
});

var weeks = document.getElementsByName('periodicity')[3];
weeks.addEventListener('click', function(){
    remove_value();
    document.getElementById('minutes').setAttribute('class', 'hidden');
    document.getElementById('hours').setAttribute('class', 'hidden');
    document.getElementById('days').setAttribute('class', 'hidden');
    document.getElementById('months').setAttribute('class', 'hidden');
    document.getElementById('years').setAttribute('class', 'hidden');
    document.getElementById('weeks').removeAttribute('class');

    for(var i=0; i<6; i++){
        if(i != 3){
            document.getElementsByName('periodicity')[i].removeAttribute('checked');
        }
    }
    weeks.setAttribute('checked', 'checked');
    document.getElementById('at_week').value = "1";
    document.getElementById('year').removeAttribute('required');
    document.getElementById('day').setAttribute('required', 'required');
});

var months = document.getElementsByName('periodicity')[4];
months.addEventListener('click', function(){
    remove_value();
    document.getElementById('minutes').setAttribute('class', 'hidden');
    document.getElementById('hours').setAttribute('class', 'hidden');
    document.getElementById('days').setAttribute('class', 'hidden');
    document.getElementById('weeks').setAttribute('class', 'hidden');
    document.getElementById('years').setAttribute('class', 'hidden');
    document.getElementById('months').removeAttribute('class');

    for(var i=0; i<6; i++){
        if(i != 4){
            document.getElementsByName('periodicity')[i].removeAttribute('checked');
        }
    }
    months.setAttribute('checked', 'checked');
    document.getElementById('on_month_day').value = "1";
    document.getElementById('day').removeAttribute('required');
    document.getElementById('year').removeAttribute('required');
});

var years = document.getElementsByName('periodicity')[5];
years.addEventListener('click', function(){
    remove_value();
    document.getElementById('minutes').setAttribute('class', 'hidden');
    document.getElementById('hours').setAttribute('class', 'hidden');
    document.getElementById('days').setAttribute('class', 'hidden');
    document.getElementById('weeks').setAttribute('class', 'hidden');
    document.getElementById('months').setAttribute('class', 'hidden');
    document.getElementById('years').removeAttribute('class');

    for(var i=0; i<6; i++){
        if(i != 5){
            document.getElementsByName('periodicity')[i].removeAttribute('checked');
        }
    }
    years.setAttribute('checked', 'checked');
    document.getElementsByName('on_month_day2')[0].value = "1";
    document.getElementById('day').removeAttribute('required');
    document.getElementById('year').setAttribute('required', 'required');
});

// Funciones de los días de la semana.

function remove_active(posc){
    for(var i=2; i<9; i++){
        if(i != posc){
            document.getElementsByClassName('nav-link')[i].removeAttribute('style');
        }
    }
}
function Txt(txt){
    document.getElementById('confirmation').textContent = txt;
    document.getElementById('confirmation').setAttribute('class', 'container');
}
function day_value(dayValue){
    dayValue.setAttribute('style', 'background-color: #1e4072; color: white');
    document.getElementById('day').value = dayValue.textContent;
    if(document.getElementsByName('at_week')[0].value != null 
        && document.getElementById('date1').value != null 
        && document.getElementById('date2').value != "" 
        && document.getElementById('time1').value != null 
        && document.getElementById('time2').value != "" 
        && document.getElementById('day').value != ""){
            txt = 'Cada '+
                document.getElementById('at_week').value+
                ' semana(s) el día '+
                document.getElementById('day').value+
                ' de cada mes, comienza '+
                document.getElementById('date1').value+
                ' a las '+
                document.getElementById('time1').value+
                'hrs';
            Txt(txt);
    }else {
        document.getElementById('confirmation').setAttribute('class', 'hidden');
    }
}

var sunday = document.getElementsByClassName('nav-link')[2];
sunday.addEventListener('click', function(){
    remove_active(2);
    day_value(sunday);
});
var monday = document.getElementsByClassName('nav-link')[3];
monday.addEventListener('click', function(){
    remove_active(3);
    day_value(monday);
});
var tuesday = document.getElementsByClassName('nav-link')[4];
tuesday.addEventListener('click', function(){
    remove_active(4);
    day_value(tuesday);
});
var wednesday = document.getElementsByClassName('nav-link')[5];
wednesday.addEventListener('click', function(){
    remove_active(5);
    day_value(wednesday);
});
var thursday = document.getElementsByClassName('nav-link')[6];
thursday.addEventListener('click', function(){
    remove_active(6);
    day_value(thursday);
});
var friday = document.getElementsByClassName('nav-link')[7];
friday.addEventListener('click', function(){
    remove_active(7);
    day_value(friday);
});
var saturday = document.getElementsByClassName('nav-link')[8];
saturday.addEventListener('click', function(){
    remove_active(8);
    day_value(saturday);
});

// Funciones de los meses del año.

function remove_active_month(posc){
    for(var i=9; i<21; i++){
        if(i != posc){
            document.getElementsByClassName('nav-link')[i].removeAttribute('style');
        }
    }
}
function month_value(monthValue){
    monthValue.setAttribute('style', 'background-color: #1e4072; color: white');
    document.getElementById('year').value = monthValue.textContent;
    if(document.getElementsByName('on_month_day2')[0].value != null 
        && document.getElementById('date1').value != null 
        && document.getElementById('date2').value != "" 
        && document.getElementById('time1').value != null 
        && document.getElementById('time2').value != "" 
        && document.getElementById('year').value != ""){
            txt = 'Cada día '+
                document.getElementsByName('on_month_day2')[0].value+
                ' del mes '+
                document.getElementById('year').value+
                ' de cada año, comienza '+
                document.getElementById('date1').value+
                ' a las '+
                document.getElementById('time1').value+
                'hrs';
            Txt(txt);
    }else {
        document.getElementById('confirmation').setAttribute('class', 'hidden');
    }
}

var january = document.getElementsByClassName('nav-link')[9];
january.addEventListener('click', function(){
    remove_active_month(9);
    month_value(january);
});
var february = document.getElementsByClassName('nav-link')[10];
february.addEventListener('click', function(){
    remove_active_month(10);
    month_value(february);
});
var march = document.getElementsByClassName('nav-link')[11];
march.addEventListener('click', function(){
    remove_active_month(11);
    month_value(march);
});
var april = document.getElementsByClassName('nav-link')[12];
april.addEventListener('click', function(){
    remove_active_month(12);
    month_value(april);
});
var may = document.getElementsByClassName('nav-link')[13];
may.addEventListener('click', function(){
    remove_active_month(13);
    month_value(may);
});
var june = document.getElementsByClassName('nav-link')[14];
june.addEventListener('click', function(){
    remove_active_month(14);
    month_value(june);
});
var july = document.getElementsByClassName('nav-link')[15];
july.addEventListener('click', function(){
    remove_active_month(15);
    month_value(july);
});
var august = document.getElementsByClassName('nav-link')[16];
august.addEventListener('click', function(){
    remove_active_month(16);
    month_value(august);
});
var september = document.getElementsByClassName('nav-link')[17];
september.addEventListener('click', function(){
    remove_active_month(17);
    month_value(september);
});
var october = document.getElementsByClassName('nav-link')[18];
october.addEventListener('click', function(){
    remove_active_month(18);
    month_value(october);
});
var november = document.getElementsByClassName('nav-link')[19];
november.addEventListener('click', function(){
    remove_active_month(19);
    month_value(november);
});
var december = document.getElementsByClassName('nav-link')[20];
december.addEventListener('click', function(){
    remove_active_month(20);
    month_value(december);
});


function footer_txt(id){
    if(document.getElementsByName(id)[0].value != null 
        && document.getElementById('date1').value != null 
        && document.getElementById('date2').value != "" 
        && document.getElementById('time1').value != null 
        && document.getElementById('time2').value != "" ){
            var txt = '';
            switch(id){
                case 'at_minutes':
                    txt = 'Cada '+
                        document.getElementById('at_minutes').value+
                        ' minuto(s), comienza '+
                        document.getElementById('date1').value+
                        ' a las '+
                        document.getElementById('time1').value+
                        'hrs';
                    Txt(txt);
                    break;
                
                case 'at_hour':
                    txt = 'Cada '+
                        document.getElementById('at_hour').value+
                        ' hora(s), comienza '+
                        document.getElementById('date1').value+
                        ' a las '+
                        document.getElementById('time1').value+
                        'hrs';
                    Txt(txt);
                    break;

                case 'on_day':
                    txt = 'Cada '+
                        document.getElementById('on_day').value+
                        ' día(s) de la semana, comienza '+
                        document.getElementById('date1').value+
                        ' a las '+
                        document.getElementById('time1').value+
                        'hrs';
                    Txt(txt);
                    break;

                case 'at_week':
                    if(document.getElementById('day').value != ""){
                        txt = 'Cada '+
                            document.getElementById('at_week').value+
                            ' semana(s) el día '+
                            document.getElementById('day').value+
                            ' de cada mes, comienza '+
                            document.getElementById('date1').value+
                            ' a las '+
                            document.getElementById('time1').value+
                            'hrs';
                        Txt(txt);
                    }
            }
    }else {
        document.getElementById('confirmation').setAttribute('class', 'hidden');
    }
}

document.getElementById('at_minutes').addEventListener('click', function(){
    footer_txt('at_minutes');
});
document.getElementById('at_hour').addEventListener('click', function(){
    footer_txt('at_hour');
});
document.getElementById('on_day').addEventListener('click', function(){
    footer_txt('on_day');
});
document.getElementById('at_week').addEventListener('click', function(){
    footer_txt('at_week');
});
document.getElementsByName('on_month_day')[0].addEventListener('click', function(){
    if(document.getElementsByName('on_month_day')[0].value != null 
        && document.getElementById('date1').value != null 
        && document.getElementById('date2').value != "" 
        && document.getElementById('time1').value != null 
        && document.getElementById('time2').value != "" ){
            txt = 'Cada día '+
                document.getElementsByName('on_month_day')[0].value+
                ' del mes, comienza '+
                document.getElementById('date1').value+
                ' a las '+
                document.getElementById('time1').value+
                'hrs';
            Txt(txt);
    }else {
        document.getElementById('confirmation').setAttribute('class', 'hidden');
    }
});
document.getElementsByName('on_month_day2')[0].addEventListener('click', function(){
    if(document.getElementsByName('on_month_day2')[0].value != null 
        && document.getElementById('date1').value != null 
        && document.getElementById('date2').value != "" 
        && document.getElementById('time1').value != null 
        && document.getElementById('time2').value != "" ){
            if(document.getElementById('year').value != ""){
                txt = 'Cada día '+
                    document.getElementsByName('on_month_day2')[0].value+
                    ' del mes '+
                    document.getElementById('year').value+
                    ' de cada año, comienza '+
                    document.getElementById('date1').value+
                    ' a las '+
                    document.getElementById('time1').value+
                    'hrs';
                Txt(txt);
            }else {
                document.getElementById('confirmation').setAttribute('class', 'hidden');
            }
    }else {
        document.getElementById('confirmation').setAttribute('class', 'hidden');
    }
});

function dates_times(){
    if( document.getElementById('date1').value != null 
        && document.getElementById('date2').value != "" 
        && document.getElementById('time1').value != null 
        && document.getElementById('time2').value != "" ){
            var id;
            for(var i=0; i<6; i++){
                var checked = document.getElementsByName('periodicity')[i];
                if(checked.getAttribute('checked') == "checked"){
                    id = checked.value;
                    console.log(id);
                    break;
                }
            }
            switch(id){
                case 'MINUTE':
                    if(document.getElementsByName('at_minutes')[0].value != null ){
                        txt = 'Cada '+
                            document.getElementById('at_minutes').value+
                            ' minuto(s), comienza '+
                            document.getElementById('date1').value+
                            ' a las '+
                            document.getElementById('time1').value+
                            'hrs';
                        Txt(txt);
                    }else {
                        document.getElementById('confirmation').setAttribute('class', 'hidden');
                    }
                    break;
                
                case 'HOUR':
                    if(document.getElementsByName('at_hour')[0].value != null ){
                        txt = 'Cada '+
                            document.getElementById('at_hour').value+
                            ' hora(s), comienza '+
                            document.getElementById('date1').value+
                            ' a las '+
                            document.getElementById('time1').value+
                            'hrs';
                        Txt(txt);
                    }else {
                        document.getElementById('confirmation').setAttribute('class', 'hidden');
                    }
                    break;

                case 'DAY':
                    if(document.getElementsByName('on_day')[0].value != null ){
                        txt = 'Cada '+
                            document.getElementById('on_day').value+
                            ' día(s) de la semana, comienza '+
                            document.getElementById('date1').value+
                            ' a las '+
                            document.getElementById('time1').value+
                            'hrs';
                        Txt(txt);
                    }else {
                        document.getElementById('confirmation').setAttribute('class', 'hidden');
                    }
                    break;

                case 'WEEK':
                    if(document.getElementById('day').value != ""
                    && document.getElementsByName('at_week')[0].value != null){
                        txt = 'Cada '+
                            document.getElementById('at_week').value+
                            ' semana(s) el día '+
                            document.getElementById('day').value+
                            ' de cada mes, comienza '+
                            document.getElementById('date1').value+
                            ' a las '+
                            document.getElementById('time1').value+
                            'hrs';
                        Txt(txt);
                    }else {
                        document.getElementById('confirmation').setAttribute('class', 'hidden');
                    }
                    break;

                case 'MONTHLY':
                    if(document.getElementsByName('on_month_day')[0].value != null){
                        txt = 'Cada día '+
                            document.getElementsByName('on_month_day')[0].value+
                            ' del mes, comienza '+
                            document.getElementById('date1').value+
                            ' a las '+
                            document.getElementById('time1').value+
                            'hrs';
                        Txt(txt);
                    }else {
                        document.getElementById('confirmation').setAttribute('class', 'hidden');
                    }
                    break;

                case 'YEARLY':
                    if(document.getElementsByName('on_month_day2')[0].value != null){
                        if(document.getElementById('year').value != ""){
                            txt = 'Cada día '+
                                document.getElementsByName('on_month_day2')[0].value+
                                ' del mes '+
                                document.getElementById('year').value+
                                ' de cada año, comienza '+
                                document.getElementById('date1').value+
                                ' a las '+
                                document.getElementById('time1').value+
                                'hrs';
                            Txt(txt);
                        }else {
                            document.getElementById('confirmation').setAttribute('class', 'hidden');
                        }
                    }else {
                        document.getElementById('confirmation').setAttribute('class', 'hidden');
                    }
                    break;
            }
    }
}
document.getElementById('date1').addEventListener('change', dates_times);
document.getElementById('date2').addEventListener('change', dates_times);
document.getElementById('time1').addEventListener('change', dates_times);
document.getElementById('time2').addEventListener('input', dates_times);

function uniq_dates_times(){
    if(document.getElementById('uniq_init_date').value != "" && document.getElementById('uniq_init_time').value != ""){
        var txt = 'Comienza el '+
            document.getElementById('uniq_init_date').value+
            ' a las '+
            document.getElementById('uniq_init_time').value+
            'hrs';
        document.getElementById('uniq_confirmation').textContent = txt;
        document.getElementById('uniq_confirmation').setAttribute('class', 'container');
    }else {
        document.getElementById('uniq_confirmation').setAttribute('class', 'hidden');
    }
}
document.getElementById('uniq_init_date').addEventListener('input', uniq_dates_times);
document.getElementById('uniq_init_time').addEventListener('input', uniq_dates_times);

function remove_unique_dates(){
    document.getElementById('uniq_confirmation').setAttribute('class', 'hidden');
    document.getElementById('uniq_init_date').value = "";
    document.getElementById('uniq_init_time').value = "";
}
document.getElementsByTagName('a')[9].addEventListener('click', remove_unique_dates);
document.getElementsByTagName('a')[10].addEventListener('click', remove_unique_dates);