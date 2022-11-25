import pandas as pd
from settings import INPUT_DIR, OUTPUT_DIR, EMAIL_SUFFIX, DEFAULT_AUDIENCE

from enum import Enum


class UserInputColumns(Enum):
    USERNAME = "username"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"


class UserOutputColumns(Enum):
    USERNAME = "username"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    AUDIENCE = "audience"


USER_CSV_FILENAME = "user.csv"

SELECTED_COLUMNS = [
    UserInputColumns.USERNAME.value,
    UserInputColumns.FIRST_NAME.value,
    UserInputColumns.LAST_NAME.value,
    UserInputColumns.EMAIL.value,
]


def preprocessing(user_df: pd.DataFrame) -> pd.DataFrame:
    return (
        user_df.loc[:, SELECTED_COLUMNS]
        .drop_duplicates(subset=[UserInputColumns.EMAIL.value])
        .dropna(subset=[UserInputColumns.EMAIL.value])
        .fillna("")
    )


def process_email(user_df: pd.DataFrame) -> pd.DataFrame:
    for (idx, email) in enumerate(user_df.loc[:, UserOutputColumns.EMAIL.value]):
        full_name: str = email.split("@")[0]

        user_df.loc[idx, UserOutputColumns.EMAIL.value] = full_name + EMAIL_SUFFIX

        first_and_last_name = full_name.split(".")

        if (
            user_df.loc[idx, UserOutputColumns.FIRST_NAME.value] == ""
            or user_df.loc[idx, UserOutputColumns.LAST_NAME.value] == ""
        ) and len(first_and_last_name) == 2:
            user_df.loc[idx, UserOutputColumns.FIRST_NAME.value] = (
                first_and_last_name[0].capitalize().replace("_", " ")
            )
            user_df.loc[idx, UserOutputColumns.LAST_NAME.value] = (
                first_and_last_name[1].upper().replace("_", " ")
            )

    return user_df


if __name__ == "__main__":
    input_user_df: pd.DataFrame = pd.read_csv(INPUT_DIR + "/" + USER_CSV_FILENAME)

    output_user_df = preprocessing(input_user_df)
    output_user_df = process_email(output_user_df)
    output_user_df.insert(
        len(output_user_df.columns), UserOutputColumns.AUDIENCE.value, DEFAULT_AUDIENCE
    )

    output_user_df.to_csv(OUTPUT_DIR + "/" + USER_CSV_FILENAME, index=False)
