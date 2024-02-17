export default function HeathBar({ currentHealth, maxHealth }) {
    // Calculate the percentage of current health relative to max health
    const healthPercentage = (currentHealth / maxHealth) * 100;

    // Determine the color based on health percentage
    let colorClass = "";
    if (healthPercentage <= 25) {
        colorClass = "bg-red-600"; // Red for low health
    } else if (healthPercentage <= 75) {
        colorClass = "bg-yellow-400"; // Yellow for moderate health
    } else {
        colorClass = "bg-green-600"; // Green for high health
    }

    return (
        <div className="flex border-4 border-green-600 rounded-full bg-white overflow-hidden w-full">
            {/* Health bar */}
            <div
                className={`transition-all duration-1000 h-4 ${colorClass}`}
                style={{ width: `${healthPercentage}%` }}
            >
            </div>

            {/* Empty bar */}
            <div
                className="transition-all duration-1000 h-4"
                style={{ width: `${100 - healthPercentage}%` }}
            ></div>
        </div>
    );
}