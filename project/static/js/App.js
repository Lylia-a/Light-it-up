

const modeltext= document.getElementById('defaut')
// Code AJAX pour récupérer les types d'événements
$.ajax({
    type: 'GET',
    url: '/typeevent-json/',
    success: function(response) {
        console.log(response.data);
        const eventtype = response.data;

        eventtype.map(item => {
            const option = document.createElement('option');
            option.textContent = item.type_team;
            option.setAttribute('class', 'item');
            option.setAttribute('data-value', item.type_team);
            typeEvent.appendChild(option);
        });
    },
    error: function(error) {
        console.log(error);
    }
});

// Événement lorsqu'un type d'événement est sélectionné
typeEvent.addEventListener('change', e => {
    console.log(e.target.value);
    selectedtype = e.target.value; // Utiliser la variable globale
    
    modeltext.textContent="voici les dates dispo"
    // Code AJAX pour récupérer les dates en fonction du type d'événement sélectionné
    $.ajax({
        type: 'GET',
        url: `team-json/${selectedtype}/`,
        success: function(response) {
            console.log(response.data);
            const calendardata = response.data;

            // Supprimer les options précédentes
            date.innerHTML = '';

            calendardata.map(item => {
                const option = document.createElement('option');
                option.textContent = item.date_a;
                option.setAttribute('class', 'item');
                option.setAttribute('data-value', item.date_a);
                date.appendChild(option);
            });
            $('#eventDate').datepicker({
                beforeShowDay: function(date) {
                    var stringDate = $.datepicker.formatDate('yy-mm-dd', date);
                    
                    // Vérifier si la date est dans la liste des dates non disponibles
                    var isDateAvailable = calendardata.some(item => item.date_a === stringDate);
                    
                    // Inverser la valeur pour masquer les dates non disponibles
                    return !isDateAvailable;
                },
                onSelect: function(dateText, inst) {
                    selectedDate = dateText;
                    console.log("Date sélectionnée :", selectedDate);
                },
            });
        },
        
        error: function(error) {
            console.log(error);
        }
    });
});










//Pour les heures: 
if (isDateAvailable) {
    selectedDate = formattedDate;
}

$.ajax({
    type: 'GET',
    url: `/heure-json/${selectedtype}/${selectedDate}/`,
    success: function(response) {
        console.log(response.data);
        const heureData = response.data;

        // Supprimer les options précédentes
        eventTime.innerHTML = '';

        heureData.map(item => {
            const option = document.createElement('option');
            option.textContent = item.heure;
            option.setAttribute('class', 'item');
            option.setAttribute('data-value', item.heure);
            eventTime.appendChild(option);
        });
    },
    error: function(error) {
        console.log(error);
    }
});