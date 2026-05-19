import { appConfig } from "./config.js"
const loginForm = document.getElementById("loginForm")
const loginInput = document.getElementById("password")
const loginButton = document.getElementById("loginSubmit")
const errorMessage = document.getElementById("loginError")
const talkForm = document.getElementById("talkForm")
const textarea = document.getElementById("speech")
const speechError = document.getElementById("speechError")
const speechSuccess = document.getElementById("speechSuccess")
const talkButton = document.getElementById("talkButton")


loginForm.addEventListener("submit", async (event) => {
    event.preventDefault()
    loginInput.disabled = true
    loginButton.disabled = true
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    const password = data["password"]

    const fetchURL = new URL("login", appConfig.apiUrl)
    try {
        const res = await fetch(fetchURL, {
            method: "POST", body: JSON.stringify({
                password
            }), headers: {
                "Content-type": "application/json"
            }
        })
        if (!res.ok) {
            if (res.status === 401) {
                setLoginError("incorrect password")
                return
            }
            setLoginError("an unknown error occurred")
            return
        }
        // Should just return a string
        const resBody = await res.json()
        localStorage.setItem(appConfig.apiKeyStorage, resBody)
    } catch (e) {
        setLoginError("an unknown error occurred")
        return
    }

    loginInput.disabled = false
    loginInput.value = ""
    loginButton.disabled = false
    loginForm.classList.add("hide")
    talkForm.classList.remove("hide")
})

loginForm.addEventListener("focusout", (event) => {
    errorMessage.innerText = ""
    errorMessage.classList.add("hide")
})

function setLoginError(message) {
    errorMessage.innerText = message
    errorMessage.classList.remove("hide")
    loginInput.disabled = false
    loginButton.disabled = false
}

function setSpeechError(message) {
    speechError.innerText = message
    speechError.classList.remove("hide")
    textarea.disabled = false
    talkButton.disabled = false
}

talkForm.addEventListener("submit", async (event) => {
    event.preventDefault()
    textarea.disabled = true
    talkButton.disabled = true
    const speech = textarea.value.trim()

    // Validate speech
    if (speech === "") {
        setSpeechError("say something to me")
        return
    }

    const fetchURL = new URL("speech", appConfig.apiUrl)

    try {
        const res = await fetch(fetchURL, {
            method: "POST",
            body: JSON.stringify({ speech }),
            headers: {
                "Content-type": "application/json",
                "x-voice-key": localStorage.getItem(appConfig.apiKeyStorage)
            }
        })
        if (!res.ok) {
            if (res.status === 401) {
                // reset this form and go back to login screen
                textarea.value = ""
                textarea.disabled = false
                talkButton.disabled = false
                speechError.classList.add("hide")
                speechSuccess.classList.add("hide")
                talkForm.classList.add("hide")
                loginForm.classList.remove("hide")
                return
            }
            // Otherwise we just throw an error
            setSpeechError("an unknown error occurred")
            return
        }
    } catch (e) {
        setSpeechError("an unknown error occurred")
        return
    }

    // If everything is fine, we send a success message
    speechError.innerText = ""
    speechError.classList.add("hide")
    textarea.value = ""
    textarea.disabled = false
    talkButton.disabled = false
    speechSuccess.innerText = "i received your message"
    speechSuccess.classList.remove("hide")

})

talkForm.addEventListener("focusout", (event) => {
    speechError.innerText = ""
    speechError.classList.add("hide")
    speechSuccess.innerText = ""
    speechSuccess.classList.add("hide")
})
