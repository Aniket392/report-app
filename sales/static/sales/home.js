const reportBtn = document.getElementById("report-btn")
const resetBtn = document.getElementById("reset-btn")
const img = document.getElementById("img")
const modeBody = document.getElementById("modal-body")
const alertBox = document.getElementById("alert-box")

const reportForm = document.getElementById("report-form")
const searchForm = document.getElementById("search-form")
const reportName = document.getElementById("id_name")
const reportRemarks = document.getElementById("id_remarks")
const csrf = document.getElementsByName("csrfmiddlewaretoken")[0]["value"]


function handleAlerts(type,msg) {
    alertBox.innerHTML = `
                <div class="alert alert-${type}" role="alert">
                    ${msg}
                </div>`
}

if(img){
    reportBtn.classList.remove("not-visible")
}

reportBtn.addEventListener("click", ()=>{
    let clone = img.cloneNode(true);
    clone.setAttribute("class","w-100")
    clone.setAttribute("id","modal-img")
    modeBody.prepend(clone)
    reportForm.addEventListener("submit", e=>{
        e.preventDefault()
        const formData = new FormData()
        formData.append("csrfmiddlewaretoken", csrf)
        formData.append("name", reportName.value)
        formData.append("remarks", reportRemarks.value)
        formData.append("image", img.src)
        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                handleAlerts("success","Report has been generated successfully.")
                reportForm.reset()
            },
            error: function (error) {
                handleAlerts("danger","Something went wrong.")
            },
            processData:false,
            contentType:false
        })
    })

})

resetBtn.addEventListener("click", ()=>{
    location.href=resetBtn.getAttribute("data-url")
})