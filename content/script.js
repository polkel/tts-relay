import { appConfig } from "./config.js"
const loginForm = document.getElementById("loginForm")
const loginInput = document.getElementById("password")
const loginButton = document.getElementById("loginSubmit")
const errorMessage = document.getElementById("loginError")
const talkForm = document.getElementById("talkForm")

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
