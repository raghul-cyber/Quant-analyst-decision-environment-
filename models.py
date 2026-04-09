from typing import Literal, Dict, Any, List
from pydantic import BaseModel, Field, field_validator

class QADEObservation(BaseModel):
    """
    Observation model representing the state of the market and portfolio at a given step.
    """
    price_history: List[float] = Field(description="last 30 closing prices")
    """last 30 closing prices"""
    
    rsi: float = Field(description="RSI indicator 0-100")
    """RSI indicator 0-100"""
    
    macd: float = Field(description="MACD line value")
    """MACD line value"""
    
    macd_signal: float = Field(description="MACD signal line")
    """MACD signal line"""
    
    volume: float = Field(description="current volume (normalized)")
    """current volume (normalized)"""
    
    sentiment_score: float = Field(description="-1.0 to 1.0")
    """-1.0 to 1.0"""
    
    volatility: float = Field(description="annualized vol, e.g. 0.25 = 25%")
    """annualized vol, e.g. 0.25 = 25%"""
    
    portfolio_cash: float = Field(description="cash in USD")
    """cash in USD"""
    
    portfolio_shares: float = Field(description="shares held")
    """shares held"""
    
    portfolio_value: float = Field(description="total portfolio value")
    """total portfolio value"""
    
    step: int = Field(description="current step number")
    """current step number"""
    
    task_name: str = Field(description="which task is running")
    """which task is running"""

    @field_validator("sentiment_score")
    @classmethod
    def clamp_sentiment(cls, v: float) -> float:
        """Clamps the sentiment score to be within [-1.0, 1.0]."""
        return max(-1.0, min(v, 1.0))

    @field_validator("rsi")
    @classmethod
    def clamp_rsi(cls, v: float) -> float:
        """Clamps the RSI to be within [0.0, 100.0]."""
        return max(0.0, min(v, 100.0))


class QADEAction(BaseModel):
    """
    Action model representing an agent's decision in the environment.
    """
    action_type: Literal["BUY", "SELL", "HOLD"] = Field(description="Type of action to execute")
    """action type: BUY, SELL, or HOLD"""
    
    amount: float = Field(description="dollar amount or 0.0 for HOLD")
    """dollar amount or 0.0 for HOLD"""
    
    reasoning: str = Field(default="", description="agent's reasoning (optional, for logging)")
    """agent's reasoning (optional, for logging)"""

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Ensures the action amount is >= 0.0."""
        if v < 0.0:
            raise ValueError("Amount must be >= 0.0")
        return v


class QADEReward(BaseModel):
    """
    Reward model representing the feedback given to the agent.
    """
    value: float = Field(description="reward scalar this step")
    """reward scalar this step"""
    
    pnl_delta: float = Field(description="profit/loss change this step")
    """profit/loss change this step"""
    
    penalty: float = Field(description="any penalties applied")
    """any penalties applied"""
    
    bonus: float = Field(description="any bonuses applied")
    """any bonuses applied"""
    
    info: str = Field(description="human-readable reason")
    """human-readable reason"""


class StepResult(BaseModel):
    """
    Result model representing the outcome of an environment step.
    """
    observation: QADEObservation = Field(description="The new observation after the step")
    """The new observation after the step"""
    
    reward: float = Field(default=0.01, description="The reward achieved this step")
    """The reward achieved this step"""
    
    done: bool = Field(description="Whether the episode is finished")
    """Whether the episode is finished"""
    
    info: dict = Field(default_factory=dict, description="Additional context dictionary")
    """Additional metadata dictionary"""

    @field_validator("reward")
    @classmethod
    def reward_never_zero(cls, v: float) -> float:
        if v == 0.0:
            return 0.01
        if v == 1.0:
            return 0.99
        return v
