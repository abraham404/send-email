// Seleccionamos el botón de envío
const submitButton = document.getElementById('submitButton');
const submitButtonRegister = document.getElementById('submitButton_register');
const submitButtonGet = document.getElementById('submitButtonSelect');
const inputsClear = document.querySelectorAll('.clear-input');
const combobox = document.getElementById('company');

const numberEmploInput = document.getElementById('num_employee_to_register');
const nameEmploInput = document.getElementById('name_employee');
const emailEmploInput = document.getElementById('email_employee');

// Añadimos un event listener al botón para capturar el evento de clic
submitButton.addEventListener('click', async (event) => {
    event.preventDefault(); // Prevenimos cualquier acción por defecto
    submitButton.disabled = true;
    // Obtenemos los valores de los inputs
    const email = document.getElementById('email').value;
    const password = document.getElementById('pass').value;
    const company = document.getElementById('company').value;
    const period = document.getElementById('period').value;
    const year = document.getElementById('year').value;


    if (validateEmail(email) === 0 || company === 'Selecciona una empresa' || period === '0') {
        if (validateEmail(email) === 0) {
            alert('Por favor, introduce una dirección de correo válida.');
        } else if (company === 'Selecciona una empresa') {
            alert('Por favor, selecciona una empresa.');
        } else if (period === '0') {
            alert('Por favor, selecciona un periodo.');
        }
        submitButton.disabled = false;

    } else {
        const data = {
            email,
            password,
            company,
            period,
            year
        };


        try {
            // Usamos fetch con async/await para enviar los datos al backend
            const response = await fetch('/api/data', {
                method: 'POST', // Usamos el método POST
                headers: {
                    'Content-Type': 'application/json' // Indicamos que los datos son JSON
                },
                body: JSON.stringify(data) // Convertimos el objeto a JSON
            });

            const result = await response.json();
            console.log('Success:', result);
            submitButton.disabled = false;
            alert(result.msg)

        } catch (error) {
            console.error('Error:', error);
        }
    }

});


submitButtonRegister.addEventListener('click', async (event) => {
    event.preventDefault(); // Prevenimos cualquier acción por defecto

    // Obtén los elementos del DOM
    const companyEmploInput = document.getElementById('company');

    // Obtén los valores de los campos
    const number_emplo = numberEmploInput.value;
    const name_emplo = nameEmploInput.value;
    const email_emplo = emailEmploInput.value;
    const company_emplo = companyEmploInput.value;

    console.log(validateEmail(email_emplo))
    if (validateEmail(email_emplo) === 0 || company_emplo === "Selecciona una empresa") {
        if (validateEmail(email_emplo) === 0) {
            alert('Por favor, introduce una dirección de correo válida.');
        } else if (company_emplo === "Selecciona una empresa") {
            alert("Por favor seleccione una empresa")
        }

    } else {

        //console.log(`${num_employee} ${name_employee} ${email_employee} ${company_employee}`);

        const data_employee = {
            number_emplo,
            name_emplo,
            email_emplo,
            company_emplo
        };


        try {
            // Usamos fetch con async/await para enviar los datos al backend
            const response = await fetch('/api/employee', {
                method: 'POST', // Usamos el método POST
                headers: {
                    'Content-Type': 'application/json' // Indicamos que los datos son JSON
                },
                body: JSON.stringify(data_employee) // Convertimos el objeto a JSON
            });

            console.log(response);  //
            const result = await response.json();
            console.log('Success:', result);
            //submitButton.disabled = false;
            // Resetea los campos del formulario
            numberEmploInput.value = "";
            nameEmploInput.value = "";
            emailEmploInput.value = "";
            //companyEmploInput.value = "";
            alert(result.msg)

        } catch (error) {
            console.error('Error:', error);
        }

    }


})


submitButtonGet.addEventListener('click', async (event) => {
    event.preventDefault();
    // Obtener el valor del input de número de empleado
    const number_emplo = document.getElementById('num_employee').value; // Necesitas el valor, no el elemento
    const company_emplo = document.getElementById('company').value;

    try {
        // Usamos fetch con async/await para enviar los datos al backend
        const response = await fetch(`/api/employee/${number_emplo}/${company_emplo}`, { // Usamos backticks y ${}
            method: 'GET', // Usamos el método GET
            headers: {
                'Content-Type': 'application/json' // No es necesario este encabezado en GET, pero lo mantenemos por compatibilidad
            }
        });


        const result = await response.json(); // Procesamos la respuesta como JSON


        if (result.status === 'success' && result.employee) {
            const { num_employee, name, email } = result.employee;
            numberEmploInput.value = num_employee;
            nameEmploInput.value = name;
            emailEmploInput.value = email;

        } else {

            alert('No se encontro el empleado')
        }


    } catch (error) {
        console.error('Error:', error); // Manejo de errores
    }

    console.log(number_emplo.value)
})


const clearInput = () => {
    inputsClear.forEach((element) => {
        element.value = "";
    })
}



validateEmail = email => {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!emailPattern.test(email)) {
        return 0
    }
    else {
        return 1;
    }

}

combobox.addEventListener('change', function () {

    if (combobox.value == 'ctBAJA_PACK_SA_LAPQ' || combobox.value == 'ctBAJA_PACK_SA_CULQ' || combobox.value == 'ctECO_BAJA_TOURS_NM') {

        combobox.style.backgroundColor = "#c9f6d6";

    } else if ((combobox.value == 'ctECO_BAJA_TOURS_2020Q' || combobox.value == 'ctTRANSPORTE_ULPZS')) {

        combobox.style.backgroundColor = "#f6c9e9";

    } else {
        combobox.style.backgroundColor = "#FFF";
    }



})

