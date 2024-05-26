
let variable = false;

document.addEventListener('DOMContentLoaded',function(){
    const form = document.getElementById("houseForm");
    const resultdiv = document.querySelector(".result");


    form.addEventListener('submit',function(event){
        event.preventDefault();


        const formdata = new FormData(form);


        fetch('/predict_home_prices',{
            method:'POST',
            body:formdata
        })
        .then(response=>response.json())
        .then(data=>{
            resultdiv.textContent = `Estimated Price: ${data.estimated_price} Lakhs`;
        })
        .catch(error => {
            console.error('Error:', error);
            resultdiv.textContent = `An error occurred. Please try again.`;
        });

    });
});






async function onPageLoad(){
    try{
        let location_names = await fetch('http://127.0.0.1:8000/get_location_names');

        if(!location_names.ok){
            throw new Error("server is busy now");
        }

        let location_data = await location_names.json()


        let drop_menu = document.getElementById("location");
        for (const location of location_data.locations) {
            let new_option = document.createElement("option");
            new_option.text = location;
            drop_menu.appendChild(new_option);
        }
    }catch(e){
        alert("server is busy now so cities has not loaded")
    }
}


// function f1(){

//     let estprice = document.querySelector(".result")
//     let bhk_val = getBHKValue();
//     let bath_val = getBathValue();
//     let location_val = document.getElementById("location").value;
//     let sqft_val = document.getElementById("area").value;

//     const data={
//         total_sqft:sqft_val.value,
//         bhk :bhk_val,
//         bath:bath_val,
//         location: location_val
//     };


//     const url_post = "http://127.0.0.1:8000/predict_home_prices";
//     fetch(url_post, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error(`Network response was not ok (Status: ${response.status} ${response.statusText})`);
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log('Received response:', data); // Log response data
//         estprice.textContent = `Estimated Price: $${data.estimated_price}`;
//     })
//     .catch(error => console.error('Error:', error));


// }


if(!variable){
    window.onload = onPageLoad()
    variable=true;
}







