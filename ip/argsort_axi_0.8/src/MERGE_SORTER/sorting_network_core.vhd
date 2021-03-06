-----------------------------------------------------------------------------------
--!     @file    sorting_network_core.vhd
--!     @brief   Sorting Network Core Module :
--!     @version 0.7.0
--!     @date    2020/10/30
--!     @author  Ichiro Kawazome <ichiro_k@ca2.so-net.ne.jp>
-----------------------------------------------------------------------------------
--
--      Copyright (C) 2020 Ichiro Kawazome
--      All rights reserved.
--
--      Redistribution and use in source and binary forms, with or without
--      modification, are permitted provided that the following conditions
--      are met:
--
--        1. Redistributions of source code must retain the above copyright
--           notice, this list of conditions and the following disclaimer.
--
--        2. Redistributions in binary form must reproduce the above copyright
--           notice, this list of conditions and the following disclaimer in
--           the documentation and/or other materials provided with the
--           distribution.
--
--      THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
--      "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
--      LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
--      A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
--      OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
--      SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
--      LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
--      DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
--      THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
--      (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
--      OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--
-----------------------------------------------------------------------------------
library ieee;
use     ieee.std_logic_1164.all;
library Merge_Sorter;
use     Merge_Sorter.Word;
use     Merge_Sorter.Sorting_Network;
entity  Sorting_Network_Core is
    generic (
        NETWORK_PARAM   :  Sorting_Network.Param_Type := Sorting_Network.Param_Null;
        WORD_PARAM      :  Word.Param_Type            := Word.Default_Param;
        INFO_BITS       :  integer :=  3
    );
    port (
        CLK             :  in  std_logic;
        RST             :  in  std_logic;
        CLR             :  in  std_logic;
        I_WORD          :  in  std_logic_vector(NETWORK_PARAM.Size*WORD_PARAM.BITS-1 downto 0);
        I_INFO          :  in  std_logic_vector(INFO_BITS-1 downto 0) := (others => '0');
        I_VALID         :  in  std_logic;
        I_READY         :  out std_logic;
        O_WORD          :  out std_logic_vector(NETWORK_PARAM.Size*WORD_PARAM.BITS-1 downto 0);
        O_INFO          :  out std_logic_vector(INFO_BITS-1 downto 0);
        O_VALID         :  out std_logic;
        O_READY         :  in  std_logic;
        BUSY            :  out std_logic
    );
end Sorting_Network_Core;
-----------------------------------------------------------------------------------
--
-----------------------------------------------------------------------------------
library ieee;
use     ieee.std_logic_1164.all;
use     ieee.numeric_std.all;
library Merge_Sorter;
use     Merge_Sorter.Word;
use     Merge_Sorter.Sorting_Network;
use     Merge_Sorter.Core_Components.Word_Compare;
library PipeWork;
use     PipeWork.Components.PIPELINE_REGISTER;
architecture RTL of Sorting_Network_Core is
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    constant  STAGE_OPENER      :  integer := NETWORK_PARAM.Stage_Lo - 1;
    constant  STAGE_FIRST       :  integer := NETWORK_PARAM.Stage_Lo;
    constant  STAGE_LAST        :  integer := NETWORK_PARAM.Stage_Hi;
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    subtype   WORD_TYPE         is std_logic_vector (WORD_PARAM.BITS-1 downto 0);
    type      STAGE_WORD_TYPE   is array (NETWORK_PARAM.Lo to NETWORK_PARAM.Hi) of WORD_TYPE;
    type      STAGE_WORD_VECTOR is array (integer range <>) of STAGE_WORD_TYPE;
    signal    stage_word        :  STAGE_WORD_VECTOR(STAGE_OPENER to STAGE_LAST);
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    subtype   STAGE_INFO_TYPE   is std_logic_vector (INFO_BITS-1 downto 0);
    type      STAGE_INFO_VECTOR is array (integer range <>) of STAGE_INFO_TYPE;
    signal    stage_info        :  STAGE_INFO_VECTOR(STAGE_OPENER to STAGE_LAST);
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    signal    stage_valid       :  std_logic_vector (STAGE_OPENER to STAGE_LAST);
    signal    stage_ready       :  std_logic_vector (STAGE_OPENER to STAGE_LAST);
    signal    stage_busy        :  std_logic_vector (STAGE_OPENER to STAGE_LAST);
    constant  STAGE_BUSY_ALL0   :  std_logic_vector (STAGE_OPENER to STAGE_LAST) := (others => '0');
begin
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    OPENER: block
    begin
        NET: for i in 0 to NETWORK_PARAM.Size-1 generate
            stage_word(STAGE_OPENER)(NETWORK_PARAM.Lo+i) <= I_WORD((i+1)*WORD_PARAM.BITS-1 downto i*WORD_PARAM.BITS);
        end generate;
        stage_info (STAGE_OPENER) <= I_INFO;
        stage_valid(STAGE_OPENER) <= I_VALID;
        stage_busy (STAGE_OPENER) <= '0';
        I_READY <= stage_ready(STAGE_OPENER);
    end block;
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    MAIN: for stage in STAGE_FIRST to STAGE_LAST generate
        constant  Stage_Param   :  Sorting_Network.Stage_Type := NETWORK_PARAM.Stage_List(stage);
        signal    sorted_word   :  STAGE_WORD_TYPE;
    begin
        ---------------------------------------------------------------------------
        --
        ---------------------------------------------------------------------------
        NET: for i in NETWORK_PARAM.Lo to NETWORK_PARAM.Hi generate
            constant  STEP           :  integer := Stage_Param.Comparator_List(i).STEP;
            constant  UP             :  boolean := Stage_Param.Comparator_List(i).UP;
        begin
            XCHG: if STEP > 0 generate
                signal    comp_sel_a     :  std_logic;
                signal    comp_sel_b     :  std_logic;
                signal    swap           :  boolean;
            begin
                -------------------------------------------------------------------
                --
                -------------------------------------------------------------------
                COMP: Word_Compare                                    --
                    generic map(                                      --
                        WORD_PARAM  => WORD_PARAM                   , -- 
                        SORT_ORDER  => NETWORK_PARAM.Sort_Order       -- 
                    )                                                 -- 
                    port map (                                        --
                        CLK         => CLK                          , -- In  :
                        RST         => RST                          , -- In  :
                        CLR         => CLR                          , -- In  :
                        A_WORD      => stage_word(stage-1)(i     )  , -- In  :
                        B_WORD      => stage_word(stage-1)(i+STEP)  , -- In  :
                        VALID       => '1'                          , -- In  :
                        READY       => open                         , -- Out :
                        SEL_A       => comp_sel_a                   , -- Out :
                        SEL_B       => comp_sel_b                     -- Out :
                    );                                                --
                swap <= (comp_sel_b = '1' and UP = TRUE ) or
                        (comp_sel_a = '1' and UP = FALSE);
                sorted_word(i     ) <= stage_word(stage-1)(i+STEP) when (swap) else
                                       stage_word(stage-1)(i     );
                sorted_word(i+STEP) <= stage_word(stage-1)(i     ) when (swap) else
                                       stage_word(stage-1)(i+STEP);
            end generate;
            PASS: if STEP = 0 generate
                sorted_word(i     ) <= stage_word(stage-1)(i     );
            end generate;
        end generate;
        ---------------------------------------------------------------------------
        --
        ---------------------------------------------------------------------------
        REGS: block
            constant  WORD_LO   :  integer := 0;
            constant  DATA_LO   :  integer := WORD_LO;
            constant  DATA_HI   :  integer := DATA_LO + NETWORK_PARAM.Size*WORD_PARAM.BITS-1;
            constant  INFO_LO   :  integer := DATA_HI + 1;
            constant  INFO_HI   :  integer := INFO_LO + INFO_BITS - 1;
            constant  WORD_HI   :  integer := INFO_HI;
            constant  WORD_BITS :  integer := WORD_HI - WORD_LO + 1;
            signal    d_word    :  std_logic_vector(WORD_BITS-1 downto 0);
            signal    q_word    :  std_logic_vector(WORD_BITS-1 downto 0);
        begin
            NET_I: for i in 0 to NETWORK_PARAM.Size-1 generate
                d_word((i+1)*WORD_PARAM.BITS-1+DATA_LO downto i*WORD_PARAM.BITS+DATA_LO)
                    <= sorted_word(i+NETWORK_PARAM.Lo);
            end generate;
            d_word(INFO_HI downto INFO_LO) <= stage_info(stage-1);
            Q: PIPELINE_REGISTER                            -- 
                generic map (                               -- 
                    WORD_BITS   => WORD_BITS,               -- 
                    QUEUE_SIZE  => Stage_Param.QUEUE_SIZE   -- 
                )                                           -- 
                port map (                                  -- 
                    CLK         => CLK                    , -- In  :
                    RST         => RST                    , -- In  :
                    CLR         => CLR                    , -- In  :
                    I_WORD      => d_word                 , -- In  :
                    I_VAL       => stage_valid(stage-1)   , -- In  :
                    I_RDY       => stage_ready(stage-1)   , -- Out :
                    Q_WORD      => q_word                 , -- Out :
                    Q_VAL       => stage_valid(stage  )   , -- Out :
                    Q_RDY       => stage_ready(stage  )   , -- In  :
                    VALID       => open                   , -- Out :
                    BUSY        => stage_busy (stage  )     -- 
                );
            NET_O: for i in 0 to NETWORK_PARAM.Size-1 generate
                stage_word(stage)(i+NETWORK_PARAM.Lo)
                    <= q_word((i+1)*WORD_PARAM.BITS-1+DATA_LO downto i*WORD_PARAM.BITS+DATA_LO);
            end generate;
            stage_info(stage) <= q_word(INFO_HI downto INFO_LO);
        end block;
    end generate;
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    OUTLET: block
    begin
        NET: for i in 0 to NETWORK_PARAM.Size-1 generate
            O_WORD((i+1)*WORD_PARAM.BITS-1 downto i*WORD_PARAM.BITS) <= stage_word(STAGE_LAST)(NETWORK_PARAM.Lo+i);
        end generate;
        O_INFO  <= stage_info (STAGE_LAST);
        O_VALID <= stage_valid(STAGE_LAST);
        stage_ready(STAGE_LAST) <= O_READY;
    end block;
    -------------------------------------------------------------------------------
    --
    -------------------------------------------------------------------------------
    BUSY <= '1' when (stage_busy /= STAGE_BUSY_ALL0) else '0';
end RTL;
