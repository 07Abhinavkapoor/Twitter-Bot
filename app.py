import tweepy
import config
import time
import tbot


class TwitterBot:
    """
    To create and run a twitter bot.

    Methods:
    authorize - To verify the user.
    get_last_mention_id - To get the last mention id, which is already seen.
    write_last_mention_id - To update the last seen mention id.
    activate_bot - To activate the bot.
    perform_actions - Take appropriate action on the mention.
    check_for_activation_trigger - To see if the mention text contains the phrase to which the bot will write a reply.
    """

    def __init__(self):
        self.api = self.authorize()

    def authorize(self):
        """
        To verify the user.

        Parameters: None

        Returns tweepy.API object.
        """
        auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        return tweepy.API(auth)

    def get_last_mention_id(self):
        """
        To get the last seen mention id.

        Parameters: None

        Returns:
        string - The last seen mention id.
        """
        try:
            with open("last_mention_id.txt", "r") as file:
                data = file.readline().strip()
                return data

        except FileNotFoundError:
            with open("last_mention_id.txt", "a") as file:
                pass

            return self.get_last_mention_id()

    def write_last_mention_id(self, id):
        """
        To update the last seen mention id.

        Parameters:
        id(int) - The id which is to be written into the file.

        Returns: None
        """
        with open("last_mention_id.txt", "w") as file:
            file.write(str(id))

    def activate_bot(self):
        """
        To activate the twitter bot.

        Parameters: None

        Returns: None
        """
        print("Twitter Bot Activated")
        while True:
            try:
                last_id = self.get_last_mention_id()
                if last_id == "":
                    mentions = self.api.mentions_timeline()
                else:
                    mentions = self.api.mentions_timeline(int(last_id))

                for mention in reversed(mentions):
                    self.perform_action(mention)

            except tweepy.TweepError:
                # If an exception occurs, generally if will be tweepy.RateLimitError and in that case the bot will sleep for 15 minutes.
                time.sleep(60 * 15)

    def perform_action(self, mention):
        """
        To perform certains actions to the mention.

        If the mention contains a particular phrase then write a responce to that tweet else retweet the mention tweet.
        Like all the mention tweets.

        Parameters:
        mentions(tweepy.models.ResultSet) - Contains all the data about the mention tweet.

        Returns: None
        """
        mention_id = mention.id
        mention_text = mention.text

        if self.check_for_activation_trigger(mention_text):
            reply = f"@{mention.user.screen_name} {tbot.responce}"
            self.api.update_status(reply, mention_id)
        else:
            self.api.retweet(mention_id)
        self.write_last_mention_id(mention_id)
        self.api.create_favorite(mention_id)
        print(f"Mention-id cleared {mention_id}")

        time.sleep(15)

    def check_for_activation_trigger(self, mention_text):
        """
        To check if the mention tweet contains a certain phrase.

        Parameters:
        mention_text(string) - The text in which we have to check for the phrase.

        Returns:
        boolean - True if the phrase is present else False.
        """
        activation_trigger_present = False

        if len(tbot.phrase.split()) == 1:
            if tbot.phrase.lower() in mention_text.lower().split():
                activation_trigger_present = True
        else:
            if tbot.phrase.lower() in mention_text.lower():
                activation_trigger_present = True

        return activation_trigger_present


if __name__ == "__main__":
    twitter_bot = TwitterBot()
    twitter_bot.activate_bot()
