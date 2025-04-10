async function submitForm(e) {
    const form = e.target;
    const formData = new FormData(form);
    const data = {
        url: formData.get('url'),
        custom_code: formData.get('custom_code') || undefined
    };

    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Failed to create short URL');
        }

        const result = await response.json();
        this.result = window.location.origin + '/' + result.short_code;
        this.error = null;
        form.reset();
    } catch (err) {
        this.error = err.message;
        this.result = null;
    }
}