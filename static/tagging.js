/* tagging.js */
// Updated to streamline save + navigation
console.log("🔥 tagging.js is live!");

function setSavingStatus(text, color, isError = false) {
    const status = document.getElementById("save-status");
    if (!status) return;
    status.textContent = text;
    status.style.backgroundColor = color;
    status.style.display = "inline-block";
    if (!isError && !text.includes("Saving…")) {
        setTimeout(() => {
            if (status.textContent === text) {
                status.style.display = "none";
            }
        }, 2500);
    }
}

function saveCurrentTags(callback, isNavigation = false) {
    const form = document.getElementById("tag-form");
    if (!form) return;
    const formElements = form.elements;
    const isRejected = formElements.rejected?.checked || false;
    const isOffensive = formElements.reject_reason?.value === "offensive" || false;
    const jsonData = {
        image_id: form.dataset.imageId || "",
        primary_element: formElements.primary_element?.value || "",
        secondary_element: formElements.secondary_element?.value || "",
        primary_principle: formElements.primary_principle?.value || "",
        secondary_principle: formElements.secondary_principle?.value || "",
        notes: formElements.notes?.value || "",
        image_quality: Array.from(formElements.image_quality || []).find(r => r.checked)?.value || "",
        issues: Array.from(formElements.issues || []).filter(cb => cb.checked).map(cb => cb.value),
        rejected: isRejected,
        offensive: isOffensive
    };
    setSavingStatus("Saving…", "#f59e0b");
    fetch("/api/save-tag", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
    })
    .then(res => {
        console.log("🔥 Server Response Status:", res.status);
        if (!res.ok) {
            return res.text().then(text => { throw new Error(`Save failed: ${res.status} ${res.statusText}. ${text}`); });
        }
        return res.json();
    })
    .then(data => {
        console.log("✅ Save successful! Server returned:", data);
        setSavingStatus("✅ Saved!", "#22c55e");
        if (callback) callback(true);
    })
    .catch(err => {
        console.error("❌ Save error:", err);
        setSavingStatus(`❌ ${err.message}`, "#ef4444", true);
        if (callback) callback(false);
    });
}

function navigate(direction) {
    console.log(`Navigating ${direction}...`);
    window.location.href = `/tag?direction=${direction}`;
}

function saveTags(callback) {
    saveCurrentTags((success) => {
        if (!success) console.error('Save failed');
        if (callback) callback(success);
    }, true);
}

document.addEventListener("DOMContentLoaded", () => {
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const saveTagsBtn = document.getElementById("saveTagsBtn");
    const rejectBtn = document.getElementById("rejectBtn");
    const markOffensiveBtn = document.getElementById("markOffensiveBtn");
    const rejectedCheckbox = document.getElementById("rejected-checkbox");
    const rejectReason = document.getElementById("reject-reason");

    prevBtn?.addEventListener("click", (e) => { e.preventDefault(); navigate('prev'); });
    saveTagsBtn?.addEventListener("click", (e) => { e.preventDefault(); rejectedCheckbox.checked=false; rejectReason.value=""; saveTags(ok => ok && navigate('next')); });
    nextBtn?.addEventListener("click", (e) => { e.preventDefault(); navigate('next'); });
    rejectBtn?.addEventListener("click", (e) => { e.preventDefault(); rejectedCheckbox.checked=true; rejectReason.value=""; saveTags(ok => ok && navigate('next')); });
    markOffensiveBtn?.addEventListener("click", (e) => { e.preventDefault(); rejectedCheckbox.checked=true; rejectReason.value="offensive"; saveTags(ok => ok && navigate('next')); });

    document.querySelectorAll("select, input[type=radio], input[type=checkbox], textarea")
        .forEach(el => el.addEventListener("change", () => saveCurrentTags()));
});
