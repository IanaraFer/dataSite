"""
Enhanced data processing following coding instructions
Scalable data handling for different pricing tiers
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, Tuple
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class ScalableDataProcessor:
    """
    Scalable data processor following coding guidelines
    Handles different file sizes based on pricing tiers
    """
    
    def __init__(self, pricing_tier: str = "professional"):
        self.pricing_tier = pricing_tier
        self.limits = self._get_tier_limits()
        
    def _get_tier_limits(self) -> Dict[str, Any]:
        """Get limits based on pricing tier"""
        tier_limits = {
            "essential": {"max_mb": 50, "max_rows": 50_000, "chunk_size": 10_000},
            "professional": {"max_mb": 200, "max_rows": 500_000, "chunk_size": 50_000},
            "business": {"max_mb": 500, "max_rows": 2_000_000, "chunk_size": 100_000},
            "enterprise": {"max_mb": 2000, "max_rows": 10_000_000, "chunk_size": 250_000}
        }
        return tier_limits.get(self.pricing_tier, tier_limits["professional"])
    
    def validate_file_size(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate file size against tier limits
        Following validation best practices from coding instructions
        """
        try:
            file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
            
            if file_size_mb > self.limits["max_mb"]:
                return False, f"File size ({file_size_mb:.1f}MB) exceeds {self.pricing_tier} plan limit ({self.limits['max_mb']}MB)"
            
            return True, f"File size OK: {file_size_mb:.1f}MB"
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return False, f"File validation error: {str(e)}"
    
    def load_data_optimized(self, file_path: str) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
        """
        Load data with optimization based on file size
        Following performance optimization from coding instructions
        """
        start_time = time.time()
        processing_info = {"method": "standard", "chunks_processed": 0, "optimization_applied": []}
        
        try:
            # Check file size first
            is_valid, message = self.validate_file_size(file_path)
            if not is_valid:
                return None, {"error": message}
            
            file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
            
            # Choose processing method based on file size
            if file_size_mb <= 50:
                # Standard processing for small files
                df = pd.read_csv(file_path)
                processing_info["method"] = "standard"
                
            elif file_size_mb <= 200:
                # Optimized processing for medium files
                df = pd.read_csv(file_path, low_memory=False)
                df = self._optimize_dtypes(df)
                processing_info["method"] = "optimized"
                processing_info["optimization_applied"].append("dtype_optimization")
                
            else:
                # Chunked processing for large files
                df = self._process_in_chunks(file_path)
                processing_info["method"] = "chunked"
                processing_info["optimization_applied"].append("chunked_processing")
            
            # Validate row count
            if len(df) > self.limits["max_rows"]:
                # Truncate if necessary (or offer sampling)
                df = df.head(self.limits["max_rows"])
                processing_info["warning"] = f"Dataset truncated to {self.limits['max_rows']} rows"
            
            processing_info["rows"] = len(df)
            processing_info["columns"] = len(df.columns)
            processing_info["processing_time"] = time.time() - start_time
            processing_info["memory_usage_mb"] = df.memory_usage(deep=True).sum() / (1024 * 1024)
            
            logger.info(f"Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
            return df, processing_info
            
        except Exception as e:
            logger.error(f"Data loading error: {str(e)}")
            return None, {"error": f"Data loading error: {str(e)}"}
    
    def _optimize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize data types to reduce memory usage
        Following performance optimization from coding instructions
        """
        try:
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Try to convert to numeric
                    numeric_series = pd.to_numeric(df[col], errors='ignore')
                    if not numeric_series.equals(df[col]):
                        df[col] = numeric_series
                
                elif df[col].dtype in ['int64', 'int32']:
                    # Downcast integers
                    df[col] = pd.to_numeric(df[col], downcast='integer')
                
                elif df[col].dtype in ['float64', 'float32']:
                    # Downcast floats
                    df[col] = pd.to_numeric(df[col], downcast='float')
            
            return df
            
        except Exception as e:
            logger.warning(f"Dtype optimization failed: {str(e)}")
            return df
    
    def _process_in_chunks(self, file_path: str) -> pd.DataFrame:
        """
        Process large files in chunks
        Following scalability best practices from coding instructions
        """
        chunk_list = []
        chunk_size = self.limits["chunk_size"]
        
        try:
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                # Process each chunk
                chunk = self._optimize_dtypes(chunk)
                chunk_list.append(chunk)
                
                # Stop if we reach row limit
                total_rows = sum(len(c) for c in chunk_list)
                if total_rows >= self.limits["max_rows"]:
                    break
            
            # Combine chunks
            df = pd.concat(chunk_list, ignore_index=True)
            return df.head(self.limits["max_rows"])  # Ensure we don't exceed limits
            
        except Exception as e:
            logger.error(f"Chunked processing error: {str(e)}")
            raise