/*************l.,********************************************************************************************//**
* @file ADC/Continuous_Potentiometer/main.c
* @version $Rev:: 4646 $
* @date $Date:: 2020-03-04 #$
* @brief Main program.
*************************************************************************************************************
* @attention
*
* Firmware Disclaimer Information
*
* 1. The customer hereby acknowledges and agrees that the program technical documentation, including the
* code, which is supplied by Holtek Semiconductor Inc., (hereinafter referred to as "HOLTEK") is the
* proprietary and confidential intellectual property of HOLTEK, and is protected by copyright law and
* other intellectual property laws.
*
* 2. The customer hereby acknowledges and agrees that the program technical documentation, including the
* code, is confidential information belonging to HOLTEK, and must not be disclosed to any third parties
* other than HOLTEK and the customer.
*
* 3. The program technical documentation, including the code, is provided "as is" and for customer reference
* only. After delivery by HOLTEK, the customer shall use the program technical documentation, including
* the code, at their own risk. HOLTEK disclaims any expressed, implied or statutory warranties, including
* the warranties of merchantability, satisfactory quality and fitness for a particular purpose.
*
* <h2><center>Copyright (C) Holtek Semiconductor Inc. All rights reserved</center></h2>
************************************************************************************************************/

/*
Following parts are removed.
1. Audio Sampling.
2. Delay
*/

/* Includes ------------------------------------------------------------------------------------------------*/
#include "ht32.h"
#include "ht32_board.h"
#include "ht32_board_config.h"
/** @addtogroup HT32_Series_Peripheral_Examples HT32 Peripheral Examples
* @{
*/
/** @addtogroup ADC_Examples ADC
* @{
*/
/** @addtogroup Continuous_Potentiometer
* @{
*/
/* Private function prototypes -----------------------------------------------------------------------------*/
void Phase0Process(void);
void MODE01Parameters(void);
void MODE0Parameters(void);
void MODE1Parameters(void);
void SignalStablePowerMeter(void);
void SignalAmplitudeComparison(void);
void CompareResult(void);
void ADC_MainRoutineA(void);
void ADC_MainRoutineB(void);
void GPIO_Configuration(void);
void ADC_Configuration(void);
static void __Delay(u32 count);

/* Global variables ----------------------------------------------------------------------------------------*/
u64 n=0; //Time index for function SignalStablePowerMeter
u32 gADC_Result[3]; //ADC output 0-2
u32 MS0C = 0; //Microphone State 0 Counter
u32 MS1C = 0; //Microphone State 1 Counter
u32 MS2C = 0; //Microphone State 2 Counter
u32 MSCMV = 2; //Microphone State Counter Maximum Value
u32 LSignalAverageValue=0;//mV
u32 RSignalAverageValue=0;//mV
u32 VT = 20; //Volume Trigger (VT)(mV) turns on the system only when someone is speaking
u32 EVPR = 1000; //Equal value power ratio: The difference tolerant between two signal regarding them as same volume
u32 EVAR = 30; //Equal value ampiltude ratio: The difference tolerant between two signal regarding them as same volume
u32 LMicSample; //Taking sample from ADC output 0
u32 RMicSample; //Taking sample from ADC output 1
u32 i=0; //for loop flag
u32 j=0; //for loop flag
u8 MicrophoneState=0; //Either be 1, 2, 3; 1=>L>R , 2=>L=R, 3=>L<R
int VolumeCompareMode=0; //0: Default&Power / 1: Simple Amplitude
float PLn=0.0; //Power value for function SignalStablePowerMeter
float PRn=0.0; //Power value for function SignalStablePowerMeter
float PLn1=0.0; //Power value for function SignalStablePowerMeter
float PRn1=0.0; //Power value for function SignalStablePowerMeter
float alpha=0.99; //Coefficient for function SignalStablePowerMeter //Need modified to be user typed
float SPSB=0.1; //Coefficient determine Stable Power Signal Bias for function SignalStablePowerMeter //Need modified to be user typed
volatile bool gADC_CycleEndOfConversion;

/* Global functions ----------------------------------------------------------------------------------------*/
/*********************************************************************************************************//**
* @brief Main program.
* @retval None
***********************************************************************************************************/
int main(void)
{
    RETARGET_Configuration(); //USART Initialization
    GPIO_Configuration(); /* GPIO Initialization */
    ADC_Configuration();/* ADC Initialization */
    ADC_Cmd(HTCFG_ADC_PORT, ENABLE);/* Enable ADC */
    ADC_SoftwareStartConvCmd(HTCFG_ADC_PORT, ENABLE);/* Software trigger to start ADC conversion */
		
    GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_7, 1);
    GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_3, 1);
		
    /* Phase 0: Getting user input values */
    Phase0Process();
    if(VolumeCompareMode!=0 && VolumeCompareMode!=1 && VolumeCompareMode!=2 && VolumeCompareMode!=3)
    {
       printf("\rPlease reset and type either 0 or 1.\n\r");
       while(1);
    }
    printf("\r\n\r");
    
	    /* Phase 1: Getting value for parameters.*/
    if(VolumeCompareMode==0) MODE0Parameters();
		else if(VolumeCompareMode==1) MODE1Parameters();
		else printf("\r\n\r");
    
	    /* Phase 2: Judging microphone volume in realtime */
    printf("\rComparing volume between MicL and MicR....\n\r");
    while(1)
    {
			ADC_MainRoutineB();
      CompareResult();
    }
}

/* Private functions ---------------------------------------------------------------------------------------*/
/*********************************************************************************************************//**
* @brief Mode selection
* @param VolumeCompareMode: Modes to compare microphone signal
*   This parameter can be one of the following values:
*     @arg 0: power comparism
*     @arg 1: amplitude comparism
*     @arg 2: power comparism with default parameters
*     @arg 3: amplitude comparism with default parameters
* @retval None
***********************************************************************************************************/
void Phase0Process(void){
	printf("\r\n\r\n");
	printf("\r====================================================================================================================================================\n\r");
	printf("\r====================================================================================================================================================\n\r");
	printf("\rProgramming starting...\n\r");
	/*Select volume comparing mode.*/
	printf("\rAvailable volume compare modes:\n\rType 0 for POWER analysis (default mode)\r\nType 1 for SIMPLEAMPLITUDE analysis\n\rType 2 for POWER analysis with default parameters\n\rType 3 for SIMPLE AMPLITUDE analysis with default parameters\n\r");
	printf("\r***** Press Backspace for default value *****\n\r");
	printf("\rDesired volume compare mode: ");
	scanf("%d", &VolumeCompareMode);
}

/*********************************************************************************************************//**
* @brief Get parameters from user
* @param alpha: alpha in formula
* @param SPSB: power difference between P(n) and P(n+1)
* @param UserDefinedDelay: Delay
* @retval None
***********************************************************************************************************/
void MODE0Parameters(void)
{
	printf("\r\n\r");
	printf("\rGathering essential parameters...\n\r");
	printf("\r\n\r");
	printf("\r***** Make sure Local Echo in Tera Term is checked *****\n\r");
	printf("\r***** Make sure DC voltage supply is plugged in *****\n\r");
	printf("\r***** Press Backspace for default value *****\n\r");
	printf("\r\n\r");
	printf("\rPlease type in desired alpha value as float (default: 0.99/close to 1): ");
	scanf("%f", &alpha);
	printf("\r\n\r(1/2)\t\t\t\t\t\t\t\t\tTarge value: %4f\n\r", alpha);
	printf("\r\n\r");
	printf("\rPlease type in desired SPSB value as float (default: 0.1/close to 0): ");
	scanf("%f", &SPSB);
	printf("\r\n\r(2/2)\t\t\t\t\t\t\t\t\tTarge value: %4f\n\r", SPSB);
    /*
	printf("\r\n\r");
	printf("\rPlease type in desired delay value between each volume compare (default: 50/Range: 0-100): ");
	scanf("%d", &UserDefinedDelay);
	printf("\r\n\r(3/3)=============================================================Targe value: %4d\n\r", UserDefinedDelay);
	printf("\r\n\r");
    */
}

/*********************************************************************************************************//**
* @brief Get parameters from user
* @param UserDefinedDelay: Delay
* @retval None
***********************************************************************************************************/
void MODE1Parameters(void)
{
	printf("\r\n\r");
	printf("\r\n\r");
	printf("\r***** Make sure Local Echo in Tera Term is checked *****\n\r");
	printf("\r***** Make sure DC voltage supply is plugged in *****\n\r");
  printf("\r***** Press Backspace for default value *****\n\r");
    /*
	printf("\rPlease type in desired delay value between each volume compare (default: 50/Range: 0-100): ");
	scanf("%d", &UserDefinedDelay);
	printf("\r\n\r(1/1)=============================================================Targe value: %4d\n\r", UserDefinedDelay);
	printf("\r\n\r");
    */
}

/*********************************************************************************************************//**
* @brief Calculating the stabled power measured from single microphone. This function will loop itself until power is stable.
* @func Pn1 = Pn*alpha+(1-alpha)(signal function)^2.
* @func signal function = L-C or R-C.
* @param Pn1: PLn1 & PRn1 is power at time index equals to (n+1)
* @param Pn: PLn & PRn is power at time index equals to (n)
* @param n: Time Index
* @retval None
***********************************************************************************************************/
void SignalStablePowerMeter(void)
{
   int L=0, R=0, LC=LSignalAverageValue, RC=RSignalAverageValue, TimeIndex=n, LRDiff = 0;
   float PLnBuffer=0, PLn1Buffer=0, PRnBuffer=0, PRn1Buffer=0, LRatio = 0, RRatio = 0;
   PLn=1; PRn=1; PLn1=1; PRn1=1;
	
   for (n=0; n<2147483647; n++)
   {
     TimeIndex=n+1;
     L=(int)gADC_Result[0];
		 R=(int)gADC_Result[1];
     PLn1=alpha*PLn+(1-alpha)*(((float)L-(float)LC)*((float)L-(float)LC));
     PRn1=alpha*PRn+(1-alpha)*(((float)R-(float)RC)*((float)R-(float)RC));
		 LRatio = (PLn1-PLn)/PLn;
		 RRatio = (PRn1-PRn)/PRn;
     printf("\rTimeIndex/L/R/LBias/RBias/PLn/PLn1/PRn/PRn1/LRatio/RRatio: %5d, %4d, %4d, %5d, %5d, %15.6f,%15.6f, %15.6f, %15.6f, %15.6f, %15.6f ", TimeIndex, L, R, L-LC, R-RC, PLnBuffer, PLn1Buffer, PRnBuffer, PRn1Buffer, LRatio, RRatio);
     //printf("\r\n\r");//create new line for mode 1
		 PLnBuffer=PLn; PLn1Buffer=PLn1; PRnBuffer=PRn; PRn1Buffer=PRn1;
     /*Break when measured power is considered stable.*/
     if(LRatio<=SPSB || RRatio<=SPSB)break;
     PLn=PLn1; PRn=PRn1;
   }
	 
	 /*Power difference*/
	 LRDiff = PRn1Buffer - PLn1Buffer - (RC-LC);
	 if (LRDiff<0) LRDiff = -LRDiff;
   printf("\n\rLRDiff/EVPR: %5d/%5d", LRDiff, EVPR);
	 
	 /*Judge microphone state*/
	 if (L-LC > VT || R-RC > VT){
			if (PLn1Buffer>PRn1Buffer && LRDiff>EVPR) MS1C++;
			if(PLn1Buffer<PRn1Buffer && LRDiff>EVPR) MS2C++;
	 }else{
			MS0C++;
	 }
}

/*********************************************************************************************************//**
* @brief Signal amplitude/volume comparison.
* @retval None
***********************************************************************************************************/
void SignalAmplitudeComparison(void)
{
  int L=(int)gADC_Result[0], R=(int)gADC_Result[1], LC=LSignalAverageValue, RC=RSignalAverageValue, LRDiff=0;
  s32 LBias=L-LC, RBias=R-RC;
  
	/*Turn negative value positive */
  if (LBias<0) LBias=-LBias;
  if (RBias<0) RBias=-RBias;
	
	/*Amplitude difference*/
	LRDiff = LBias - RBias - (RC-LC);
	if (LRDiff<0) LRDiff = -LRDiff;
  
	/*Judge microphone state */
	if (L-LC > VT || R-RC > VT){
			if (LBias>RBias && LRDiff>EVAR) MS1C++;
			if(RBias<LBias && LRDiff>EVAR) MS2C++;
	 }else{
			MS0C++;
	 }
	 
	 printf("\rSampling LMic:%5d | Sampling RMic:%5d | LBias: %5d | RBias: %5d | LRDiff/EVAR: %5d/%5d ", L, R, L-LC, R-RC, LRDiff, EVAR);
}

/*********************************************************************************************************//**
* @brief Print compared result
* @retval Signal centrol gPotentiometerLevel
***********************************************************************************************************/
void CompareResult()
{
  if (MS0C>MSCMV){
		MicrophoneState=0;
		if (MS0C!=0)MS0C--;
	}

	if (MS1C>MSCMV){
		MicrophoneState=1;
		if (MS1C!=0)MS1C--;
	}
	
	if (MS2C>MSCMV){
		MicrophoneState=2;
		if (MS2C!=0)MS2C--;
	}
	
	switch (MicrophoneState)
    {
    case 0:
				if (VolumeCompareMode == 0 || VolumeCompareMode == 2)printf("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t=====L=R\n\r");
        if (VolumeCompareMode == 1 || VolumeCompareMode == 3)printf("\t\t\t\t\t=====L=R");
				GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_7, 0);
        GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_3, 0);
        break;
		case 1:
        if (VolumeCompareMode == 0 || VolumeCompareMode == 2)printf("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t=====L>R\n\r");
        if (VolumeCompareMode == 1 || VolumeCompareMode == 3)printf("\t\t\t\t\t=====L>R");
        GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_7, 1);
        GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_3, 0);
        break;
    case 2:
        if (VolumeCompareMode == 0 || VolumeCompareMode == 2)printf("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t=====L<R\n\r");
        if (VolumeCompareMode == 1 || VolumeCompareMode == 3)printf("\t\t\t\t\t=====L<R");
        GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_7, 0);
        GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_3, 1);
        break;
    }
}

/*********************************************************************************************************//**
* @brief ADC A main routine.
* @retval None
***********************************************************************************************************/
void ADC_MainRoutineA(void)
{
  LMicSample = (int)gADC_Result[0];
  RMicSample = (int)gADC_Result[1];
  if (gADC_CycleEndOfConversion) gADC_CycleEndOfConversion = FALSE;
}

/*********************************************************************************************************//**
* @brief ADC B main routine.
* @retval None
***********************************************************************************************************/
void ADC_MainRoutineB(void)
{
  if(VolumeCompareMode==0 || VolumeCompareMode==2)SignalStablePowerMeter(); //Default mode.
  if(VolumeCompareMode==1 || VolumeCompareMode==3)SignalAmplitudeComparison();
  if (gADC_CycleEndOfConversion) gADC_CycleEndOfConversion = FALSE;
}

/*********************************************************************************************************//**
* @brief Configure the GPIO as output mode.
* @retval None
***********************************************************************************************************/
void GPIO_Configuration(void)
{
  { /* Enable peripheral clock */
    CKCU_PeripClockConfig_TypeDef CKCUClock = {{ 0 }};
    CKCUClock.Bit.AFIO = 1;
    CKCUClock.Bit.PA = 1;
    CKCU_PeripClockConfig(CKCUClock, ENABLE);
  
    /* Configure GPIO as input mode */
    /* Configure AFIO mode as GPIO */
    AFIO_GPxConfig(GPIO_PA, AFIO_PIN_2, AFIO_FUN_GPIO);//not working
    AFIO_GPxConfig(GPIO_PA, AFIO_PIN_3, AFIO_FUN_GPIO);
		AFIO_GPxConfig(GPIO_PA, AFIO_PIN_7, AFIO_FUN_GPIO);
    /* Configure GPIO pull resistor */
    GPIO_PullResistorConfig(HT_GPIOA, GPIO_PIN_2, GPIO_PR_DOWN);
    GPIO_PullResistorConfig(HT_GPIOA, GPIO_PIN_3, GPIO_PR_DOWN);
		GPIO_PullResistorConfig(HT_GPIOA, GPIO_PIN_7, GPIO_PR_DOWN);
    /* Default value RESET/SET */
    GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_2, RESET);
    GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_3, RESET);
		GPIO_WriteOutBits(HT_GPIOA, GPIO_PIN_7, RESET);
    /* Configure GPIO direction as output */
    GPIO_DirectionConfig(HT_GPIOA, GPIO_PIN_2, GPIO_DIR_OUT);
    GPIO_DirectionConfig(HT_GPIOA, GPIO_PIN_3, GPIO_DIR_OUT);
		GPIO_DirectionConfig(HT_GPIOA, GPIO_PIN_7, GPIO_DIR_OUT);
  }
}

/*********************************************************************************************************//**
* @brief ADC Configuration.
* @retval None
***********************************************************************************************************/
void ADC_Configuration(void)
{
  { /* Enable peripheral clock */
    CKCU_PeripClockConfig_TypeDef CKCUClock = {{ 0 }};
    CKCUClock.Bit.AFIO = 1;
    CKCUClock.Bit.HTCFG_ADC_IPN = 1;
		CKCU_PeripClockConfig(CKCUClock, ENABLE);
  }
    /* Configure AFIO mode as ADC function */
  AFIO_GPxConfig(HTCFG_VR_GPIO_ID, HTCFG_VR_AFIO_PIN, HTCFG_ADC_AFIO_MODE);
  AFIO_GPxConfig(HTCFG_AD2_GPIO_ID, HTCFG_AD2_AFIO_PIN, HTCFG_ADC_AFIO_MODE);
  AFIO_GPxConfig(HTCFG_AD3_GPIO_ID, HTCFG_AD3_AFIO_PIN, HTCFG_ADC_AFIO_MODE);
  { /* ADC related settings */
    /* CK_ADC frequency is set to (CK_AHB / 64) */
	  CKCU_SetADCnPrescaler(HTCFG_ADC_CKCU_ADCPRE, CKCU_ADCPRE_DIV64);
    /* Continuous mode, sequence length = 3, subgroup length = 0
    */
    ADC_RegularGroupConfig(HTCFG_ADC_PORT, CONTINUOUS_MODE, 3, 0);
    /* ADC conversion time = (Sampling time + Latency) / CK_ADC = (1.5 + ADST + 12.5) / CK_ADC */
    /* Set ADST = 0, sampling time = 1.5 + ADST */
    #if (LIBCFG_ADC_SAMPLE_TIME_BY_CH)
    // The sampling time is set by the last parameter of the function "ADC_RegularChannelConfig()".
    #else
    ADC_SamplingTimeConfig(HTCFG_ADC_PORT, 0);
    #endif
    /* Set ADC conversion sequence as channel n */
    ADC_RegularChannelConfig(HTCFG_ADC_PORT, HTCFG_VR_ADC_CH, 0, 0);
    ADC_RegularChannelConfig(HTCFG_ADC_PORT, HTCFG_AD2_ADC_CH, 1, 0);
    ADC_RegularChannelConfig(HTCFG_ADC_PORT, HTCFG_AD3_ADC_CH, 2, 0);
    /* Set software trigger as ADC trigger source */
    ADC_RegularTrigConfig(HTCFG_ADC_PORT, ADC_TRIG_SOFTWARE);
  }
    /* Enable ADC cycle and subgroup end of conversion interrupt*/
  ADC_IntConfig(HTCFG_ADC_PORT, ADC_INT_CYCLE_EOC, ENABLE);
    /* Enable the ADC interrupts */
  NVIC_EnableIRQ(HTCFG_ADC_IRQn);
}

#if (HT32_LIB_DEBUG == 1)
/*********************************************************************************************************//**
* @brief Report both the error name of the source file and the source line number.
* @param filename: pointer to the source file name.
* @param uline: error line source number.
* @retval None
***********************************************************************************************************/
void assert_error(u8* filename, u32 uline)
{
/*
This function is called by IP library that the invalid parameters has been passed to the library API.
Debug message can be added here.
Example: printf("Parameter Error: file %s on line %d\r\n", filename, uline);
*/
while (1)
{
}
}
#endif
/* Private functions ---------------------------------------------------------------------------------------*/
/*********************************************************************************************************//**
* @brief delay function
* @param count: delay count for loop
* @retval None
***********************************************************************************************************/
static void __Delay(u32 count)
{
  while (count--)
  {
    __NOP(); // Prevent delay loop be optimized
  }
}
/**
 * @}
 */
/**
 * @}
 */
/**
 * @}
 */
