"use server";

export default async function chatCompletion(prompt: string, user: string) {
    const response = await fetch(`${process.env.API_URL}/v1/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
            "prompt": prompt, 
            "user_name": user 
        }),
    });
    const data = await response.json();
    console.log(data);
    return data;
}