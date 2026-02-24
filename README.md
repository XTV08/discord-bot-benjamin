# Benjamin - Contested Territory Scoreboard Bot

Benjamin is a custom Discord bot designed to automate tile tracking and score management for Contested Territory events. It features a reaction-based scoreboard, automated reset timers, and administrative commands for clan leaders.

## 🚀 Features

* **Reaction-Based Tracking:** Users can click reactions on a central message to increment their tile counts (Normal, Relic, and Banner).
* **Automatic Score Calculation:** * Normal Tiles: 1 point
    * Relic/Banner Tiles: 2 points
* **Scheduled Announcements:** Automatically notifies the server when a new CT event starts and resets scores every two weeks.
* **Administrative Control:** Restricted commands for "Leader" and "Assistant Mayor" roles to manually adjust scores or update rules.
* **Live Scoreboard:** A single, continuously updated message displaying all member scores in an easy-to-read format.

---

## 🛠 Installation & Setup

1.  **Dependencies:**
    Install the required Python libraries:
    ```bash
    pip install discord.py pytz
    ```

2.  **Configuration:**
    Open the script and update the following variables with your specific Discord IDs:
    * `count_channel_id`: The ID of the channel where the scoreboard lives.
    * `notification_channel_id`: The ID for @everyone announcements.
    * `rules_channel_id`: The ID for the rules channel.
    * `DISCORD_API_TOKEN`: Your bot's secret token.

3.  **Run the Bot:**
    ```bash
    python benjamin_bot.py
    ```

---

## 🕹 Commands

### Management Commands
*Requires 'Leader' or 'Assistant Mayor' roles.*

| Command | Usage | Description |
| :--- | :--- | :--- |
| `!scoreboard` | `!scoreboard` | Generates a new active scoreboard message. |
| `!set_normal` | `!set_normal @user 5` | Manually sets a user's normal tile count. |
| `!set_relic` | `!set_relic @user 2` | Manually sets a user's relic tile count. |
| `!set_banner` | `!set_banner @user 3` | Manually sets a user's banner tile count. |
| `!reset_tiles` | `!reset_tiles` | Resets everyone's scores to 0. |
| `!rules` | `!rules "New Text"` | Updates the text in the designated rules channel. |
| `!announcement`| `!announcement "Text"` | Sends a formatted announcement embed. |
| `!poll` | `!poll "Title" ✅ ❌` | Creates a poll with up to 5 reaction options. |

### System Commands
* `!instructions_scoreboard`: Posts the "How-to-use" guide for members.
* `!recount_scoreboard [ID]`: Connects the bot to an existing message ID to act as the scoreboard.
* `!terminate`: Shuts down the bot (Owner only).

---

## 📊 Score Calculation Logic

The "Tile Score" is calculated using the following formula:

$$Score = Normal + 2 \times (Relic + Banner)$$

---

## ⚠️ Important Notes
* **Intents:** This bot requires `intents.all()` to be enabled in the [Discord Developer Portal](https://discord.com/developers/applications).
* **Self-Correction:** Users are responsible for their own scores. If a user makes a mistake, an admin must use a `set` command to correct it.
* **Persistence:** This version uses in-memory dictionaries (`normal_count`, etc.). If the bot restarts, scores will reset unless the `!recount_scoreboard` or manual setup is used.
