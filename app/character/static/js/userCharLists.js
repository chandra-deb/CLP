const {ref, reactive, onMounted} = Vue;

const listName = ref('')
const errorMsg = ref('')
const isInputBoxOpen = ref(false)
const isDisplayDeleteModal = ref(false)
const isDisplayEditModal = ref(false)
const isDisplayCreateModal = ref(false)


let grabbedListName = ''
let grabbedListId = NaN
const inputValue = ref('')
const isLoading = ref(false)

function pinList(listId){
    console.log(listId, 'From pinLIst')
    try {
        listId = parseInt(listId)
    } catch (e) {
        console.error(e)
    }
    const data = {
        listId: listId,
    }
    isLoading.value = true
    axios.post('/character/pin_list', data)
        .then(function (response) {
            console.log(response.data);
            window.location.reload()
        })
        .catch(function (error) {
            console.log(error);
            errorMsg.value = error
        });

}
function unpinList(listId){
        console.log(listId, 'From pinLIst')
    try {
        listId = parseInt(listId)
    } catch (e) {
        console.error(e)
    }
    const data = {
        listId: listId,
    }
    isLoading.value = true
    axios.post('/character/unpin_list', data)
        .then(function (response) {
            console.log(response.data);
            window.location.reload()
        })
        .catch(function (error) {
            console.log(error);
            errorMsg.value = error
        });

}

function toggleInputBox() {
    isInputBoxOpen.value = !isInputBoxOpen.value;
}

function showCreateListModal() {
    isDisplayCreateModal.value = true
}

function closeCreateListModal() {
    isDisplayCreateModal.value = false
    errorMsg.value = ''
    inputValue.value = ''
}

function confirmCreateList() {
    console.log(inputValue.value)

    const trimmedListName = inputValue.value.trim()
    inputValue.value = trimmedListName

    if (trimmedListName.length < 6) {
        errorMsg.value = 'List name length must be more than 6 characters'
        return;
    }
    isDisplayCreateModal.value = false
    isLoading.value = true
    makeSubmission()

}

function showEditModal(listName, listId) {
    isDisplayEditModal.value = true
    inputValue.value = listName
    grabbedListName = listName
    grabbedListId = listId
}

function closeEditModal() {
    isDisplayEditModal.value = false
    inputValue.value = ''
    errorMsg.value = ''
}


function confirmEdit() {
    let trimmedValue = inputValue.value.trim()
    if (trimmedValue === grabbedListName) {
        console.log('I am elses')
        errorMsg.value = 'You made no changes.';
    } else {
        if (trimmedValue.length > 4) {
            errorMsg.value = ''
            isLoading.value = true
            isDisplayEditModal.value = false
            setInterval(
                () => {
                },
                10000,
            )
            window.location.reload();
        } else {
            console.log('I am elses')
            errorMsg.value = 'List Name must contain more than 4 letters';
            inputValue.value = trimmedValue
        }
    }

}

function toggleDeleteModal() {
    isDisplayDeleteModal.value = !isDisplayDeleteModal.value;
    errorMsg.value = ''
    inputValue.value = ''
}

function showDeleteModal(listName, listId) {
    isDisplayDeleteModal.value = true
    grabbedListName = listName
    grabbedListId = listId

}

function confirmDelete() {
    if (grabbedListName === inputValue.value) {
        console.log('Deleting list: ', grabbedListName);
        errorMsg.value = ''
        isLoading.value = true
        isDisplayDeleteModal.value = false
        setInterval(
            () => {
            },
            10000,
        )
        window.location.reload();
    } else {
        errorMsg.value = 'Please write the correct list name.';
    }
}

function createList() {
    const trimmedListName = listName.value.trim()
    listName.value = trimmedListName

    if (trimmedListName.length < 6) {
        errorMsg.value = 'List name length must be more than 6 characters'
        return;
    }
    makeSubmission()
    listName.value = ''
    errorMsg.value = ''

}

function makeSubmission() {
    let parentListId = NaN
    try {
        parentListId = parseInt(list_id)
    } catch (e) {
        console.error(e)
    }
    const data = {
        listName: inputValue.value,
        parentListId: parentListId,
    }
    axios.post('/character/create_list', data)
        .then(function (response) {
            console.log(response.data);
            window.location.reload()
        })
        .catch(function (error) {
            console.log(error);
            errorMsg.value = error
        });
}

const App = {
    setup() {
        return {
            listName,
            errorMsg,
            isInputBoxOpen,
            isDisplayDeleteModal,
            isDisplayEditModal,
            isDisplayCreateModal,
            grabbedListName,
            inputValue,
            isLoading,
            toggleInputBox,
            toggleDeleteModal,
            createList,
            makeSubmission,
            showDeleteModal,
            confirmDelete,
            confirmEdit,
            showEditModal,
            closeEditModal,
            showCreateListModal,
            closeCreateListModal,
            confirmCreateList,
            pinList,
            unpinList,
        }
    },

    delimiters: ['[[', ']]']
}

Vue.createApp(App).mount('#app')