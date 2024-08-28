const {ref, reactive, onMounted} = Vue;

const text = ref('')
const reportData = ref({})
const isAdding = ref(false)
const isShowReport = ref(false)
let listId = NaN
const selectedMatches = ref([])
const errorMsg = ref('')

function confirmAddition() {
    let ids = selectedMatches.value.map(match => match.id)
    if(selectedMatches.value.length === 0) {
        console.log('No Selected Matches')
        isShowReport.value = false
        isAdding.value = false
        history.back()
        return
    }
    console.log(ids)
    const data = {
        by: 'ids',
        listId: listId,
        charIds: ids
    }
    axios.post('/character/add_chars', data)
        .then(function (response) {
            let data = response.data;
            isShowReport.value = false
            history.back()
        })
        .catch(function (error) {
            console.log(error);
        });
}

function selectMatch(match) {
    let done = false
    for (let i = 0; i < selectedMatches.value.length; i++) {
        if (selectedMatches.value[i].character === match.character && selectedMatches.value[i].id === match.id) {
            selectedMatches.value.splice(i, 1)
            console.log('Spliced')
            done = true
            break;
        } else if (selectedMatches.value[i].character === match.character) {
            selectedMatches.value = selectedMatches.value.filter(selected => selected.character !== match.character)
            selectedMatches.value.push({character: match.character, id: match.id})
            done = true
            break
        }
    }
    if (done === false) {
        selectedMatches.value.push({character: match.character, id: match.id})
    }

}

function isSelected(detail) {
    const selectedMatch = selectedMatches.value.find(match => match.character === detail.character && match.id === detail.id);
    return selectedMatch !== undefined;

}

function processedText() {
    const value = text.value
    let processed = value.split(/[\s\n\r]+/);
    processed = processed.filter(item => item !== '');
    return processed;
}

function submitText(newListId) {
    listId = newListId
    makeSubmission()
}


function makeSubmission() {
    if(processedText().length === 0) {
        errorMsg.value = 'Empty Text'
        return
    }
    errorMsg.value = ''

    const data = {
        by: 'characters',
        listId: listId,
        characters: processedText()
    }
    isAdding.value = true
    axios.post('/character/add_chars', data)
        .then(function (response) {
            let data = response.data['result'];
            reportData.value = {
                addedChars: data.added_characters,
                existingChars: data.existing_characters,
                multipleMatches: data.multiple_matches,
                notFoundChars: data.not_found_characters,
            }
            isShowReport.value = true
            console.log(reportData.value)
            // window.location.reload()
        })
        .catch(function (error) {
            console.log(error);
        });
}

const App = {
    setup() {
        return {
            text,
            reportData,
            isAdding,
            isShowReport,
            selectedMatches,
            errorMsg,
            confirmAddition,
            isSelected,
            submitText,
            selectMatch,
        }
    },

    delimiters: ['[[', ']]']
}

Vue.createApp(App).mount('#app')