$(document).ready(function () {
    var InputCount=3;
    $("#AddMoreTextBox").click(function (e)
    {
            InputCount++;
            $("#InputsWrapper").append('<label></label><input type="text" name="news_food_' + InputCount + '" value="原料名 '+ InputCount +'"/> <input type="text" name="news_quan_' + InputCount + '" value="原料数量 '+ InputCount +'"/><br/><br/>');
    });
});