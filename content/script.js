import { appConfig } from "./config.js"
const form = document.querySelector("#loginForm")

form.addEventListener("submit", (event) => {
    event.preventDefault()
    const formData = new FormData(event.target)
    const data = Object.fromEntries(formData.entries())
    const speech = data["speech"]
    const fetchURL = new URL("speech", appConfig.apiUrl)

    fetch(fetchURL, {method: "POST", 
        body: JSON.stringify({
            speech
        })
    }).catch(e => console.log(e))
})
