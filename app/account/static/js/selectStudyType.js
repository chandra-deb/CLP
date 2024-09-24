const {ref, computed, onMounted} = Vue;


const isShowSelection = ref(false)
const selectedType = ref('Minutes')
const selectedValue = ref(5)
const showCustomModes = ref(false)

const wordOptions = [3, 5, 8, 10, 15, 20, 30, 60]
const timeOptions = [2, 5, 8, 10, 15]

const currentOptions = computed(() => {
    console.log(selectedType.value)
    return selectedType.value === 'Minutes' ? timeOptions : wordOptions

})

const customModes = [
    {name: 'Refresh', icon: '♻️', description: 'Refresh weak memories but stop before learning anything new.'},
    {name: 'Assumed', icon: '🔄', description: 'Check words we assume you know.'},
    {
        name: 'Repeat',
        icon: '🔁',
        description: 'Review words you have strong memories of (before you theoretically need to).'
    },
    {name: 'New', icon: '✨', description: 'Ignore weak memories and jump straight to learning new words.'},
    {name: 'Hard', icon: '🌧️', description: 'Focus on words you have trouble remembering.'}
]

const selectType = (type) => {
    selectedType.value = type
    selectedValue.value = type === 'Minutes' ? timeOptions[0] : wordOptions[0]
}

const selectMode = (mode) => {
    console.log(selectedType.value)
    if (mode === 'Custom') {
        showCustomModes.value = true
    } else {
        console.log(`Selected mode: ${mode}`)
        // Add your logic here for handling Everyday mode selection
    }
}

const selectCustomMode = (mode) => {
    console.log(`Selected custom mode: ${mode}`)
    console.log(selectedType.value)
    // Add your logic here for handling custom mode selection
}


const App = {
    setup() {
        return {
            selectedType,
            selectedValue,
            currentOptions,
            showCustomModes,
            isShowSelection,
            customModes,
            selectType,
            selectMode,
            selectCustomMode

        }
    },

    delimiters: ['[[', ']]']
}

Vue.createApp(App).mount('#app')